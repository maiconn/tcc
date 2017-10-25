@echo off

echo "iniciando compilacao..."

echo "removendo arquivos..."
cd C:\Users\MaiconM\Documents\FURB\TCC\frontend\monitor\platforms\android\build\outputs\apk\
DEL /Q android-release-unsigned.apk Monitor1.0.apk
DEL /Q Monitor1.0.apk
DEL /Q "C:\Users\MaiconM\Desktop\Monitor1.0.apk"

IF  not EXIST "C:\Users\MaiconM\Documents\FURB\TCC\frontend\monitor\platforms\android\build\outputs\apk\my-release-key.jks" (
	echo "gerando chave..."
	call "C:\Users\MaiconM\Documents\FURB\TCC\extras\GeraAPK\2_gerar_chave.bat"
) 

cd C:\Users\MaiconM\Documents\FURB\TCC\frontend\monitor  
start ionic cordova build android --release

echo "aguarde compilar para continuar..."
pause

echo "assinando apk..."
cd C:\Users\MaiconM\Documents\FURB\TCC\frontend\monitor\platforms\android\build\outputs\apk\
"%java_home%\bin\jarsigner.exe" -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.jks android-release-unsigned.apk my-alias

echo "gerando apk..."
cd C:\Users\MaiconM\Documents\FURB\TCC\frontend\monitor\platforms\android\build\outputs\apk\
"%android_home%\build-tools\25.0.3\zipalign.exe" -v 4 android-release-unsigned.apk Monitor1.0.apk

echo "verificando apk.."
call "C:\Users\MaiconM\Documents\FURB\TCC\extras\GeraAPK\5_verificar.bat"


copy "C:\Users\MaiconM\Documents\FURB\TCC\frontend\monitor\platforms\android\build\outputs\apk\Monitor1.0.apk" "C:\Users\MaiconM\Desktop\Monitor1.0.apk"

echo "apk gerada :)"
pause