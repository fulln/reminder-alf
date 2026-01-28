#!/bin/bash
# 自动升级版本号并发布
# 使用: ./release.sh [major|minor|patch]

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取当前版本号 (从 pyproject.toml 读取)
get_current_version() {
    if [ -f pyproject.toml ]; then
        grep '^version = ' pyproject.toml | head -1 | sed 's/version = "\(.*\)"/\1/'
    elif git describe --tags --abbrev=0 2>/dev/null; then
        git describe --tags --abbrev=0 | sed 's/^v//'
    else
        echo "0.0.0"
    fi
}

# 升级版本号
bump_version() {
    local version=$1
    local bump_type=$2

    IFS='.' read -r -a parts <<< "$version"
    local major="${parts[0]}"
    local minor="${parts[1]}"
    local patch="${parts[2]}"

    case $bump_type in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            echo "Unknown bump type: $bump_type"
            exit 1
            ;;
    esac

    echo "${major}.${minor}.${patch}"
}

# 从 git log 自动生成 changelog 条目
generate_changelog_entries() {
    local last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
    local commits=""

    if [ -z "$last_tag" ]; then
        # 没有 tag，获取所有提交
        commits=$(git log --pretty=format:"%s" --no-merges)
    else
        # 获取自上次 tag 以来的提交
        commits=$(git log ${last_tag}..HEAD --pretty=format:"%s" --no-merges)
    fi

    local added=()
    local changed=()
    local fixed=()
    local removed=()
    local deprecated=()
    local security=()
    local other=()

    # 分析每个 commit message
    while IFS= read -r commit; do
        # 跳过空行
        [ -z "$commit" ] && continue

        # 根据 Conventional Commits 规范分类
        case "$commit" in
            feat:*|feature:*)
                message=$(echo "$commit" | sed 's/^[^:]*: *//')
                added+=("$message")
                ;;
            fix:*|bugfix:*)
                message=$(echo "$commit" | sed 's/^[^:]*: *//')
                fixed+=("$message")
                ;;
            docs:*|doc:*)
                message=$(echo "$commit" | sed 's/^[^:]*: *//')
                changed+=("$message")
                ;;
            refactor:*|style:*|perf:*)
                message=$(echo "$commit" | sed 's/^[^:]*: *//')
                changed+=("$message")
                ;;
            remove:*|delete:*)
                message=$(echo "$commit" | sed 's/^[^:]*: *//')
                removed+=("$message")
                ;;
            deprecate:*)
                message=$(echo "$commit" | sed 's/^[^:]*: *//')
                deprecated+=("$message")
                ;;
            security:*|sec:*)
                message=$(echo "$commit" | sed 's/^[^:]*: *//')
                security+=("$message")
                ;;
            chore:*|build:*|ci:*)
                # 跳过维护性提交
                ;;
            "Bump version"*)
                # 跳过版本升级提交
                ;;
            *)
                # 其他提交归入 Changed
                other+=("$commit")
                ;;
        esac
    done <<< "$commits"

    # 生成 changelog 内容
    local changelog=""

    if [ ${#added[@]} -gt 0 ]; then
        changelog+="### Added\n"
        for item in "${added[@]}"; do
            changelog+="- $item\n"
        done
        changelog+="\n"
    fi

    if [ ${#changed[@]} -gt 0 ] || [ ${#other[@]} -gt 0 ]; then
        changelog+="### Changed\n"
        for item in "${changed[@]}"; do
            changelog+="- $item\n"
        done
        for item in "${other[@]}"; do
            changelog+="- $item\n"
        done
        changelog+="\n"
    fi

    if [ ${#deprecated[@]} -gt 0 ]; then
        changelog+="### Deprecated\n"
        for item in "${deprecated[@]}"; do
            changelog+="- $item\n"
        done
        changelog+="\n"
    fi

    if [ ${#removed[@]} -gt 0 ]; then
        changelog+="### Removed\n"
        for item in "${removed[@]}"; do
            changelog+="- $item\n"
        done
        changelog+="\n"
    fi

    if [ ${#fixed[@]} -gt 0 ]; then
        changelog+="### Fixed\n"
        for item in "${fixed[@]}"; do
            changelog+="- $item\n"
        done
        changelog+="\n"
    fi

    if [ ${#security[@]} -gt 0 ]; then
        changelog+="### Security\n"
        for item in "${security[@]}"; do
            changelog+="- $item\n"
        done
        changelog+="\n"
    fi

    echo -e "$changelog"
}

# 更新 CHANGELOG
update_changelog() {
    local version=$1
    local date=$(date +%Y-%m-%d)

    if [ ! -f CHANGELOG.md ]; then
        echo -e "${YELLOW}⚠️  CHANGELOG.md 不存在，创建新文件${NC}"
        cat > CHANGELOG.md << 'EOF'
# Changelog

All notable changes to Reminder-Alf will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

EOF
    fi

    # 生成 changelog 条目
    echo -e "${BLUE}📝 从 Git 提交自动生成 changelog...${NC}"
    local entries=$(generate_changelog_entries)

    if [ -z "$entries" ]; then
        echo -e "${YELLOW}⚠️  没有找到新的提交${NC}"
        entries="### Changed\n- Minor updates and improvements\n"
    fi

    # 创建临时文件
    local temp_file=$(mktemp)

    # 读取 CHANGELOG.md 并处理
    local in_unreleased=false
    local unreleased_replaced=false

    while IFS= read -r line; do
        if [[ $line == "## [Unreleased]" ]]; then
            # 替换 [Unreleased] 为新版本
            echo "## [$version] - $date" >> "$temp_file"
            echo "" >> "$temp_file"
            echo -e "$entries" >> "$temp_file"
            unreleased_replaced=true
            in_unreleased=true
            continue
        elif [[ $line =~ ^##\  ]] && [ "$in_unreleased" = true ]; then
            # 遇到下一个版本，结束 unreleased 部分
            in_unreleased=false
            # 添加新的 [Unreleased] 部分
            echo "## [Unreleased]" >> "$temp_file"
            echo "" >> "$temp_file"
            echo "$line" >> "$temp_file"
            continue
        elif [ "$in_unreleased" = true ]; then
            # 跳过 [Unreleased] 部分的旧内容
            continue
        fi

        echo "$line" >> "$temp_file"
    done < CHANGELOG.md

    # 如果没有找到 [Unreleased]，在文件开头添加
    if [ "$unreleased_replaced" = false ]; then
        local header_temp=$(mktemp)
        head -5 CHANGELOG.md > "$header_temp"
        echo "" >> "$header_temp"
        echo "## [Unreleased]" >> "$header_temp"
        echo "" >> "$header_temp"
        echo "## [$version] - $date" >> "$header_temp"
        echo "" >> "$header_temp"
        echo -e "$entries" >> "$header_temp"
        tail -n +6 CHANGELOG.md >> "$header_temp"
        mv "$header_temp" "$temp_file"
    fi

    mv "$temp_file" CHANGELOG.md
    echo -e "${GREEN}✅ 已更新 CHANGELOG.md${NC}"
}

# 更新 pyproject.toml 中的版本号
update_pyproject_toml() {
    local version=$1

    if [ -f pyproject.toml ]; then
        # macOS 兼容的 sed 命令
        sed -i.bak "s/^version = \"[^\"]*\"/version = \"${version}\"/" pyproject.toml
        rm -f pyproject.toml.bak
        echo -e "${GREEN}✅ 已更新 pyproject.toml${NC}"
    fi
}

# 显示帮助
show_help() {
    cat << EOF
${BLUE}🚀 Reminder-Alf 自动发布脚本${NC}

${YELLOW}使用方法:${NC}
  ./release.sh [major|minor|patch] [options]

${YELLOW}参数:${NC}
  major       主版本号升级 (1.0.0 -> 2.0.0)
  minor       次版本号升级 (1.0.0 -> 1.1.0)
  patch       补丁版本号升级 (1.0.0 -> 1.0.1)

${YELLOW}选项:${NC}
  -n, --no-push    只创建 tag，不推送到远程
  -d, --dry-run    模拟运行，不实际修改文件
  -h, --help       显示帮助信息

${YELLOW}示例:${NC}
  ./release.sh patch              # 升级补丁版本并推送
  ./release.sh minor --no-push    # 升级次版本但不推送
  ./release.sh major --dry-run    # 模拟主版本升级

${YELLOW}Git Commit 规范:${NC}
  feat:      新功能 (归入 Added)
  fix:       Bug 修复 (归入 Fixed)
  docs:      文档更新 (归入 Changed)
  refactor:  代码重构 (归入 Changed)
  perf:      性能优化 (归入 Changed)
  remove:    删除功能 (归入 Removed)
  deprecate: 废弃功能 (归入 Deprecated)
  security:  安全修复 (归入 Security)
  chore:     构建/工具 (不显示)

${YELLOW}流程:${NC}
  1. 检查工作区是否干净
  2. 从 Git commits 自动生成 changelog
  3. 升级版本号
  4. 更新 pyproject.toml、CHANGELOG.md
  5. 运行测试
  6. 构建工作流包
  7. Git commit 所有更改
  8. 创建 git tag
  9. 推送到远程 (触发 GitHub Actions)

EOF
}

# 主流程
main() {
    local bump_type=""
    local no_push=false
    local dry_run=false

    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            major|minor|patch)
                bump_type=$1
                shift
                ;;
            -n|--no-push)
                no_push=true
                shift
                ;;
            -d|--dry-run)
                dry_run=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}❌ 未知参数: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done

    # 检查必需参数
    if [ -z "$bump_type" ]; then
        echo -e "${RED}❌ 缺少版本升级类型${NC}"
        show_help
        exit 1
    fi

    echo -e "${BLUE}🚀 Reminder-Alf 自动发布${NC}"
    echo "================================"
    echo ""

    # 1. 检查工作区
    echo -e "${YELLOW}1️⃣  检查 Git 工作区...${NC}"
    if [ "$dry_run" = false ]; then
        if ! git diff-index --quiet HEAD --; then
            echo -e "${RED}❌ 工作区有未提交的修改${NC}"
            echo "请先提交或暂存修改："
            git status --short
            exit 1
        fi
    fi
    echo -e "${GREEN}✅ 工作区干净${NC}"
    echo ""

    # 2. 获取并升级版本号
    echo -e "${YELLOW}2️⃣  升级版本号...${NC}"
    current_version=$(get_current_version)
    new_version=$(bump_version "$current_version" "$bump_type")
    echo "   当前版本: ${current_version}"
    echo "   新版本:   ${new_version}"
    echo ""

    if [ "$dry_run" = true ]; then
        echo -e "${YELLOW}[模拟模式]${NC}"
        echo ""
        echo -e "${BLUE}📝 将要生成的 Changelog:${NC}"
        echo "---"
        generate_changelog_entries
        echo "---"
        exit 0
    fi

    # 3. 更新文件
    echo -e "${YELLOW}3️⃣  更新版本文件...${NC}"
    update_pyproject_toml "$new_version"
    update_changelog "$new_version"
    echo ""

    # 4. 运行测试
    echo -e "${YELLOW}4️⃣  运行测试...${NC}"
    if python3 -m pytest src/tests/ -q --tb=short; then
        echo -e "${GREEN}✅ 所有测试通过${NC}"
    else
        echo -e "${RED}❌ 测试失败，请修复后再发布${NC}"
        exit 1
    fi
    echo ""

    # 5. 构建工作流
    echo -e "${YELLOW}5️⃣  构建 Alfred 工作流...${NC}"
    if python3 scripts/build_workflow.py > /dev/null 2>&1; then
        echo -e "${GREEN}✅ 工作流构建成功${NC}"
    else
        echo -e "${RED}❌ 工作流构建失败${NC}"
        exit 1
    fi
    echo ""

    # 6. Git commit
    echo -e "${YELLOW}6️⃣  提交更改到 Git...${NC}"
    git add pyproject.toml CHANGELOG.md
    git commit -m "Bump version to ${new_version}"
    echo -e "${GREEN}✅ 已创建 commit${NC}"
    echo ""

    # 7. 创建 tag
    echo -e "${YELLOW}7️⃣  创建 Git tag...${NC}"
    git tag -a "v${new_version}" -m "Release version ${new_version}"
    echo -e "${GREEN}✅ 已创建 tag: v${new_version}${NC}"
    echo ""

    # 8. 推送到远程
    if [ "$no_push" = false ]; then
        echo -e "${YELLOW}8️⃣  推送到远程仓库...${NC}"

        # 推送 commit 到 main
        if git push origin main; then
            echo -e "${GREEN}✅ 已推送 commits 到 main${NC}"
        else
            echo -e "${RED}❌ 推送 commits 失败${NC}"
            exit 1
        fi

        # 推送 tag
        if git push origin "v${new_version}"; then
            echo -e "${GREEN}✅ 已推送 tag${NC}"
        else
            echo -e "${RED}❌ 推送 tag 失败${NC}"
            exit 1
        fi
        echo ""
    else
        echo -e "${YELLOW}⏭️  跳过推送 (--no-push)${NC}"
        echo ""
        echo -e "${BLUE}手动推送命令:${NC}"
        echo "  git push origin main"
        echo "  git push origin v${new_version}"
        echo ""
    fi

    # 完成
    echo "================================"
    echo -e "${GREEN}✅ 发布完成！${NC}"
    echo "================================"
    echo ""
    echo -e "${BLUE}版本信息:${NC}"
    echo "  版本: v${new_version}"
    echo "  Tag:  v${new_version}"
    echo ""

    if [ "$no_push" = false ]; then
        echo -e "${BLUE}GitHub Actions:${NC}"
        echo "  查看构建状态："
        REPO_URL=$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')
        echo "  https://github.com/${REPO_URL}/actions"
        echo ""
        echo -e "${BLUE}Release 页面:${NC}"
        echo "  https://github.com/${REPO_URL}/releases"
        echo ""
        echo -e "${YELLOW}💡 提示: GitHub Actions 会自动构建并发布 .alfredworkflow 文件${NC}"
    fi
    echo ""
}

# 执行主流程
main "$@"
