# פנייה לתמיכת GitHub: מחיקת קומיט שנשאר במטמון

איפה שולחים: https://support.github.com/contact, תחת Remove data / Sensitive data removal.

---

Subject: Request to purge cached commit after history rewrite (argovalex/skipper-quiz)

Hello,

I accidentally committed a third-party copyrighted document to my public repository argovalex/skipper-quiz. I have rewritten the history with git filter-repo and force-pushed all affected branches (main, redesign). The file is no longer in any branch.

The old commit is still reachable by SHA:
https://github.com/argovalex/skipper-quiz/commit/c26e6ae1cd476e71049c399b26da93a232a81832

File path: lessons/l40/sources/gmdss-study-book-2026.raw.txt

The repository has no forks, and no open pull requests reference this commit.

Please run garbage collection and remove cached views of this commit and any dangling objects that contain this file.

Thank you,
Alexander Argov
