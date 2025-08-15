# Simple demo seeding script
param(
    [int]$Missions = 3
)

$base = "http://localhost:8000"

# ping health endpoint
Invoke-WebRequest "$base/healthz" | Out-Null

# register admin if missing
try {
    $body = @{username="admin"; password="admin"} | ConvertTo-Json
    Invoke-RestMethod -Method Post -Uri "$base/auth/register" -Body $body -ContentType "application/json" | Out-Null
} catch {
    # ignore errors
}

# login to get token
$login = @{username="admin"; password="admin"} | ConvertTo-Json
$token = (Invoke-RestMethod -Method Post -Uri "$base/auth/token-json" -Body $login -ContentType "application/json").access_token
$headers = @{Authorization="Bearer $token"}

for ($i = 1; $i -le $Missions; $i++) {
    $day = (Get-Date).AddDays($i-1).ToString("yyyy-MM-dd")
    $payload = @{title="Mission $i"; day=$day} | ConvertTo-Json
    Invoke-RestMethod -Method Post -Uri "$base/missions" -Headers $headers -Body $payload -ContentType "application/json"
}
