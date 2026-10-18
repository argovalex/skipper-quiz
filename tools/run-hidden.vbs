' Runs a command with no console window and waits for it (Scheduled Tasks).
' usage: wscript.exe run-hidden.vbs <program> [args...]
' Alex 2026-10-18: scheduled .cmd/.ps1 tasks flashed empty black windows.
Dim sh, cmd, i, a
Set sh = CreateObject("WScript.Shell")
For i = 0 To WScript.Arguments.Count - 1
  a = WScript.Arguments(i)
  If InStr(a, " ") > 0 Then a = """" & a & """"
  cmd = cmd & a & " "
Next
WScript.Quit sh.Run(Trim(cmd), 0, True)
