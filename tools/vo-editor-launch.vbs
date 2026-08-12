' Hidden launcher for the SkipperQuiz VO-editor server (localhost:8899).
' Runs node with no console window. Resolves paths relative to this file,
' so it stays portable across machines. Registered as a logon Scheduled Task.
Dim fso, sh, scriptDir
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh  = CreateObject("WScript.Shell")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)   ' ...\SkipperQuiz\tools
sh.CurrentDirectory = fso.GetParentFolderName(scriptDir)      ' ...\SkipperQuiz
sh.Run "node """ & scriptDir & "\vo-editor-server.js""", 0, False
