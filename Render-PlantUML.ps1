param(
    [string]$PlantUMLFile,
    [string]$OutputFile
)

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.Web

# Read PlantUML file
if (-not (Test-Path $PlantUMLFile)) {
    Write-Error "File not found: $PlantUMLFile"
    exit 1
}

$content = Get-Content $PlantUMLFile -Raw -Encoding UTF8

# Encode for PlantUML
$bytes = [System.Text.Encoding]::UTF8.GetBytes($content)
$compressed = New-Object System.IO.MemoryStream
$gzip = New-Object System.IO.Compression.DeflateStream($compressed, [System.IO.Compression.CompressionMode]::Compress)
$gzip.Write($bytes, 0, $bytes.Length)
$gzip.Close()
$compressedBytes = $compressed.ToArray()

# Base64 encode
$base64 = [Convert]::ToBase64String($compressedBytes)

# PlantUML encoding (base64 with different alphabet)
$plantumlAlphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
$base64Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

$encoded = ""
foreach ($char in $base64.ToCharArray()) {
    $index = $base64Alphabet.IndexOf($char)
    if ($index -ge 0) {
        $encoded += $plantumlAlphabet[$index]
    } else {
        $encoded += $char
    }
}

# Build URL and fetch
$url = "http://www.plantuml.com/plantuml/png/$encoded"
Write-Host "Fetching: $url"
Write-Host "URL length: $($encoded.Length) characters"

try {
    $response = Invoke-WebRequest -Uri $url -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -OutFile $OutputFile -ErrorAction Stop
    Write-Host "✅ Successfully saved to $OutputFile"
} catch {
    Write-Error "Failed to download: $_"
    exit 1
}
