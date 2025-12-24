# Git 版本控制完整指南

## 目錄
1. [版本控制是什麼？](#版本控制是什麼)
2. [為什麼需要版本控制？](#為什麼需要版本控制)
3. [Git 基本概念](#git-基本概念)
4. [安裝與設定](#安裝與設定)
5. [基本操作指令](#基本操作指令)
6. [分支管理](#分支管理)
7. [遠端倉庫操作](#遠端倉庫操作)
8. [開發工作流程](#開發工作流程)
9. [進階技巧](#進階技巧)
10. [常見問題解決](#常見問題解決)
11. [最佳實務](#最佳實務)

## 版本控制是什麼？

版本控制系統（Version Control System, VCS）是一種記錄檔案變更歷史的工具，讓開發者能夠：
- 追蹤程式碼的每一次修改
- 多人協作開發
- 在需要時回復到之前的版本
- 管理不同版本的程式碼

Git 是目前最流行的分散式版本控制系統。

## 為什麼需要版本控制？

### 個人開發者
- **變更追蹤**：知道什麼時候修改了什麼
- **備份**：程式碼安全地儲存在本地和遠端
- **實驗功能**：可以放心嘗試新想法，失敗時能輕鬆回復
- **版本管理**：為不同版本建立標籤

### 團隊開發
- **協作**：多人同時修改同一個專案
- **衝突解決**：自動偵測和解決修改衝突
- **程式碼審查**：Pull Request 機制
- **專案管理**：追蹤功能開發進度

## Git 基本概念

### Repository（倉庫）
- 專案的根目錄，包含所有檔案和 Git 歷史
- 分為本地倉庫和遠端倉庫

### Commit（提交）
- 一次變更的快照
- 包含修改的檔案、作者、時間和描述訊息

### Branch（分支）
- 獨立的開發線路
- 允許平行開發多個功能

### Working Directory（工作目錄）
- 您正在編輯的檔案目錄

### Staging Area（暫存區）
- 準備提交的檔案區域
- 介於工作目錄和倉庫之間

## 安裝與設定

### Windows 安裝
1. 下載 Git：https://git-scm.com/download/win
2. 執行安裝程式
3. 驗證安裝：開啟命令提示字元輸入 `git --version`

### 基本設定
```bash
# 設定使用者名稱
git config --global user.name "您的姓名"

# 設定電子郵件
git config --global user.email "您的email@example.com"

# 設定預設編輯器
git config --global core.editor "code --wait"

# 檢視設定
git config --list
```

## 基本操作指令

### 初始化專案
```bash
# 初始化新倉庫
git init

# 複製現有倉庫
git clone <repository-url>
```

### 檔案狀態檢查
```bash
# 檢查檔案狀態
git status

# 檢查檔案差異
git diff

# 檢查已暫存的變更
git diff --staged
```

### 新增檔案
```bash
# 新增特定檔案
git add <filename>

# 新增所有檔案
git add .

# 互動式新增
git add -p
```

### 提交變更
```bash
# 提交已暫存的檔案
git commit -m "提交訊息"

# 新增並提交所有已追蹤的檔案
git commit -a -m "提交訊息"

# 修改最後一次提交
git commit --amend
```

### 檢視歷史
```bash
# 完整歷史
git log

# 簡潔格式
git log --oneline

# 圖形化分支歷史
git log --graph --oneline --all

# 特定檔案歷史
git log -- <filename>
```

## 標籤管理（Tag）

### 什麼是標籤？
標籤（Tag）是用來標記專案中的重要節點，通常用於標記版本發佈。Git 支援兩種標籤：

- **輕量標籤（Lightweight Tag）**：簡單的指標，指向特定提交
- **註解標籤（Annotated Tag）**：包含標籤名稱、電子郵件、日期、訊息等完整資訊

### 建立標籤
```bash
# 建立輕量標籤
git tag v1.0.0

# 建立註解標籤（推薦）
git tag -a v1.0.0 -m "Release version 1.0.0"

# 為特定提交建立標籤
git tag -a v1.0.0 <commit-hash> -m "Release version 1.0.0"
```

### 檢視標籤
```bash
# 列出所有標籤
git tag

# 檢視特定標籤資訊
git show v1.0.0

# 搜尋標籤
git tag -l "v1.*"

# 依日期排序標籤
git tag --sort=-version:refname
```

### 推送標籤到遠端
```bash
# 推送特定標籤
git push origin v1.0.0

# 推送所有標籤
git push origin --tags

# 推送所有標籤（另一種方式）
git push --tags
```

### 刪除標籤
```bash
# 刪除本地標籤
git tag -d v1.0.0

# 刪除遠端標籤
git push origin :refs/tags/v1.0.0

# 或使用更簡單的語法
git push origin --delete v1.0.0
```

### 切換到標籤
```bash
# 切換到標籤（唯讀模式）
git checkout v1.0.0

# 從標籤建立分支
git checkout -b branch-from-tag v1.0.0
```

### 版本標籤命名慣例
- **語意化版本（Semantic Versioning）**：
  - `v1.0.0` - 主要版本.次要版本.修補版本
  - `v1.0.0-alpha` - 測試版
  - `v1.0.0-beta` - 測試版
  - `v1.0.0-rc.1` - 發行候選版

- **常見標籤範例**：
  - `v1.0.0` - 穩定發佈版本
  - `v2.1.3` - 主要版本2，次要版本1，修補版本3
  - `v1.0.0-alpha.1` - 第一個 alpha 版本
  - `v1.0.0-beta.2` - 第二個 beta 版本
  - `v1.0.0-rc.1` - 第一個發行候選版本

### 標籤管理最佳實務
1. **使用註解標籤**：包含完整資訊，方便追蹤
2. **語意化版本**：遵循版本命名慣例
3. **標記穩定版本**：只在穩定版本建立標籤
4. **撰寫清晰訊息**：說明版本變更內容
5. **定期推送標籤**：確保團隊同步

### 實際應用場景
```bash
# 發佈新版本的完整流程
git checkout main
git pull origin main
git tag -a v1.1.0 -m "Add user authentication feature"
git push origin main
git push origin v1.1.0

# 部署特定版本
git checkout v1.0.0
# 進行部署操作...

# 比較兩個版本的差異
git diff v1.0.0 v1.1.0
```

## 遠端倉庫推送指南

### 遠端倉庫設定

#### 建立遠端倉庫
1. **GitHub**：前往 https://github.com/new 建立新倉庫
2. **GitLab**：前往 https://gitlab.com/projects/new 建立新倉庫
3. **其他平台**：Bitbucket、Codeberg 等

#### 設定遠端來源
```bash
# 新增遠端倉庫（使用 HTTPS）
git remote add origin https://github.com/username/repo-name.git

# 或使用 SSH（需要 SSH 金鑰設定）
git remote add origin git@github.com:username/repo-name.git

# 檢視遠端設定
git remote -v

# 重新命名遠端
git remote rename origin upstream

# 移除遠端
git remote remove origin
```

### 推送操作

#### 基本推送
```bash
# 推送主分支並設定上游分支
git push -u origin main

# 推送其他分支
git push origin feature-branch

# 強制推送（小心使用，可能覆蓋遠端變更）
git push --force-with-lease origin main
```

#### 推送標籤
```bash
# 推送單一標籤
git push origin v1.0.0

# 推送所有標籤
git push origin --tags

# 推送所有分支和標籤
git push --all --tags origin
```

#### 拉取更新
```bash
# 拉取遠端變更並合併
git pull origin main

# 只擷取遠端變更（不合併）
git fetch origin

# 拉取所有分支
git pull --all
```

### 常見推送情境

#### 首次推送專案
```bash
# 設定遠端倉庫
git remote add origin https://github.com/username/my-project.git

# 推送主分支
git push -u origin main

# 推送標籤
git push origin --tags
```

#### 推送功能分支
```bash
# 建立功能分支
git checkout -b feature/new-feature

# 開發功能並提交
git add .
git commit -m "Add new feature"

# 推送功能分支
git push -u origin feature/new-feature

# 建立 Pull Request（在 GitHub/GitLab 上）
```

#### 同步遠端變更
```bash
# 檢查遠端狀態
git status

# 拉取最新變更
git pull origin main

# 如果有衝突，手動解決後提交
git add .
git commit -m "Merge remote changes"
git push origin main
```

### 推送問題解決

#### 推送被拒絕（non-fast-forward）
```bash
# 拉取遠端變更
git pull origin main --rebase

# 或強制推送（注意：會覆蓋遠端）
git push --force-with-lease origin main
```

#### 身份驗證問題
```bash
# 使用個人存取權杖（GitHub）
git remote set-url origin https://username:token@github.com/username/repo.git

# 或設定 SSH 金鑰
ssh-keygen -t ed25519 -C "your_email@example.com"
# 將公鑰加入 GitHub SSH Keys
```

#### 大檔案推送問題
```bash
# 安裝 Git LFS（大檔案支援）
git lfs install
git lfs track "*.zip"
git add .gitattributes
git commit -m "Add Git LFS tracking"

# 或移除大檔案
git rm --cached large-file.zip
git commit -m "Remove large file"
```

### 推送最佳實務
1. **定期推送**：避免積累太多本機提交
2. **使用有意義的提交訊息**：方便追蹤變更
3. **確認分支**：推送前確認在正確分支
4. **避免強制推送**：除非確定不會影響他人
5. **設定上游分支**：使用 `-u` 設定預設推送目標

### 實際工作流程
```bash
# 日常開發流程
git checkout main
git pull origin main          # 同步最新變更
git checkout -b feature/work  # 建立功能分支
# ... 開發工作 ...
git add .
git commit -m "Implement feature"
git push origin feature/work  # 推送功能分支
# ... 建立 Pull Request ...
git checkout main
git pull origin main          # 合併後同步
```

## 分支管理

### 基本分支操作
```bash
# 檢視所有分支
git branch

# 建立新分支
git branch <branch-name>

# 切換分支
git checkout <branch-name>

# 建立並切換分支
git checkout -b <branch-name>

# 刪除分支
git branch -d <branch-name>
```

### 分支合併
```bash
# 合併分支到目前分支
git merge <branch-name>

# 互動式合併（解決衝突）
git merge --no-ff <branch-name>

# 取消合併
git merge --abort
```

### 遠端分支
```bash
# 檢視遠端分支
git branch -r

# 推送本地分支到遠端
git push origin <branch-name>

# 刪除遠端分支
git push origin --delete <branch-name>
```

## 遠端倉庫操作

### 遠端設定
```bash
# 新增遠端倉庫
git remote add origin <repository-url>

# 檢視遠端設定
git remote -v

# 重新命名遠端
git remote rename <old-name> <new-name>

# 移除遠端
git remote remove <remote-name>
```

### 推送與拉取
```bash
# 推送分支
git push origin <branch-name>

# 推送所有分支
git push --all origin

# 拉取遠端變更
git pull origin <branch-name>

# 拉取所有分支
git pull --all
```

### 同步操作
```bash
# 擷取遠端變更（不合併）
git fetch origin

# 比較本地與遠端分支差異
git log HEAD..origin/main
```

## 開發工作流程

### 基本流程
1. **建立功能分支**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **開發功能**
   - 編輯檔案
   - 測試功能

3. **提交變更**
   ```bash
   git add .
   git commit -m "實作新功能"
   ```

4. **推送分支**
   ```bash
   git push origin feature/new-feature
   ```

5. **建立 Pull Request**
   - 在 GitHub/GitLab 建立 PR
   - 等待程式碼審查

6. **合併到主分支**
   ```bash
   git checkout main
   git pull origin main
   git merge feature/new-feature
   ```

### 版本發佈流程
1. **準備發佈**
   ```bash
   git checkout main
   git pull origin main
   ```

2. **測試**
   - 執行所有測試
   - 檢查功能完整性

3. **建立版本標籤**
   ```bash
   git tag -a v1.0.0 -m "發佈版本 1.0.0"
   git push origin --tags
   ```

## 進階技巧

### 修復常見問題
```bash
# 取消暫存檔案
git reset HEAD <filename>

# 放棄工作目錄變更
git checkout -- <filename>

# 取消最近的提交（保留檔案）
git reset --soft HEAD~1

# 取消最近的提交（刪除檔案變更）
git reset --hard HEAD~1
```

### 檔案操作
```bash
# 重新命名檔案
git mv <old-name> <new-name>

# 刪除檔案
git rm <filename>

# 復原刪除的檔案
git checkout HEAD -- <filename>
```

### 歷史重寫
```bash
# 互動式變基（修改歷史）
git rebase -i HEAD~3

# 壓縮多個提交
git rebase -i --autosquash
```

### 比較與分析
```bash
# 比較分支
git diff <branch1>..<branch2>

# 誰修改了這行程式碼
git blame <filename>

# 搜尋提交訊息
git log --grep="關鍵字"
```

## 常見問題解決

### 合併衝突
當兩個分支修改同一個檔案的同一行時會發生衝突：

1. Git 會標記衝突區域
2. 手動編輯檔案解決衝突
3. 標記為已解決：
   ```bash
   git add <filename>
   git commit
   ```

### 意外提交了敏感資訊
```bash
# 修改最後提交（移除檔案）
git rm --cached <sensitive-file>
git commit --amend

# 強制推送（小心使用）
git push --force-with-lease
```

### 回復到特定版本
```bash
# 建立新提交來回復變更
git revert <commit-hash>

# 硬重置到特定版本（會遺失歷史）
git reset --hard <commit-hash>
```

## 最佳實務

### 提交習慣
- **頻繁提交**：小變更多提交
- **清晰訊息**：說明做了什麼和為什麼
- **原子提交**：每個提交只做一件事

### 分支策略
- **主分支**：`main` 或 `master`，保持穩定
- **開發分支**：`develop`，整合功能
- **功能分支**：`feature/*`，開發新功能
- **修復分支**：`hotfix/*`，緊急修復
- **發佈分支**：`release/*`，準備發佈

### 工作流程建議
1. 從 `main` 分支建立功能分支
2. 定期合併 `main` 到功能分支
3. 使用 Pull Request 進行程式碼審查
4. 刪除已合併的功能分支

### .gitignore 設定
建立 `.gitignore` 檔案排除不應追蹤的檔案：

```
# Python
__pycache__/
*.pyc
*.pyo
.env

# IDE
.vscode/
.idea/

# 作業系統
.DS_Store
Thumbs.db
```

### 團隊協作
- **統一格式**：使用 EditorConfig 或 Pre-commit hooks
- **程式碼審查**：每個 PR 至少一人審查
- **CI/CD**：自動化測試和部署
- **文件**：保持 README 和文件更新

## 學習資源

### 官方文件
- [Git 官方文件](https://git-scm.com/doc)
- [Pro Git 書籍](https://git-scm.com/book/zh-tw)

### 線上平台
- [GitHub](https://github.com)
- [GitLab](https://gitlab.com)
- [Bitbucket](https://bitbucket.org)

### 學習工具
- [GitHub Desktop](https://desktop.github.com)
- [GitKraken](https://www.gitkraken.com)
- [Sourcetree](https://www.sourcetreeapp.com)

---

這份指南涵蓋了 Git 版本控制的主要概念和操作。建議從基本指令開始練習，逐步熟悉進階功能。記住，版本控制是一種習慣，需要持續練習才能熟練。
