# Security checklist

- Do not use a GitHub account password for Git operations.
- Authenticate with GitHub CLI, OAuth, SSH, or a narrowly scoped personal access token.
- Never place tokens in remote URLs, shell history, source files, or screenshots.
- Keep `.env` ignored.
- Run a secret scan before every push.
- Rotate any key or password previously pasted into a chat or committed to a file.
- Exclude raw financial screenshots and personal avatar footage from public repositories.

Suggested local scan:

```powershell
rg -n --hidden -S "api[_-]?key|Authorization|Bearer|sk_[A-Za-z0-9_-]{12,}" . -g "!.git/**"
```

