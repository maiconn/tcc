cd C:\Users\MaiconM\Documents\FURB\TCC\frontend\monitor\platforms\android\build\outputs\apk\

"%java_home%\bin\jarsigner.exe" -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.jks android-release-unsigned.apk my-alias
