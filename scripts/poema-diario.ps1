# Configurar encoding de salida
$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Cargar variables de entorno desde .env
$envFilePath = "$PSScriptRoot\.env"
if (Test-Path $envFilePath) {
    Get-Content $envFilePath | ForEach-Object {
        if ($_ -match '^\s*([^#].*?)=(.*)$') {
            $name, $value = $matches[1].Trim(), $matches[2].Trim()
            [System.Environment]::SetEnvironmentVariable($name, $value, 'Process')
        }
    }
} else {
    Write-Host "[Vicky] No se encontró el archivo .env en $envFilePath"
}

# Función para log
function Write-Log {
    param ([string]$message)
    Add-Content -Path "$PSScriptRoot\log-vicky.txt" -Value "$(Get-Date -Format "yyyy-MM-dd HH:mm:ss") $message"
}

# Función para enviar mensaje a Telegram
function Send-TelegramMessage {
    param ([string]$message)

    $botToken = $env:BOT_TOKEN
    $chatId = $env:CHAT_ID

    $body = @{
        chat_id = $chatId
        text    = $message
        parse_mode = "Markdown"
    }

    $jsonBody = $body | ConvertTo-Json -Depth 10 -Compress

    try {
        Write-Host "[Vicky] Enviando a Telegram..."
        $response = Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/sendMessage" `
                                      -Method Post `
                                      -ContentType "application/json; charset=utf-8" `
                                      -Body $jsonBody
        Write-Host "[Vicky] Mensaje enviado correctamente 📤"
    } catch {
        Write-Host "[Vicky] Error al enviar mensaje a Telegram: $($_.Exception.Message)"
    }
}

# Ejecutar script de Vicky en Python
python "$PSScriptRoot\vicky_backup_poema.py"

Write-Host "[main] Poema del $date subido con éxito 🚀"

# Enviar mensaje por Telegram
Send-TelegramMessage -message $poemContent
