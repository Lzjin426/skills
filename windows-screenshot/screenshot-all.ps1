Add-Type -AssemblyName System.Windows.Forms,System.Drawing
$screens = [System.Windows.Forms.Screen]::AllScreens
$left = [int]::MaxValue
$top = [int]::MaxValue
$right = [int]::MinValue
$bottom = [int]::MinValue
foreach ($s in $screens) {
    $b = $s.Bounds
    if ($b.Left -lt $left) { $left = $b.Left }
    if ($b.Top -lt $top) { $top = $b.Top }
    if ($b.Right -gt $right) { $right = $b.Right }
    if ($b.Bottom -gt $bottom) { $bottom = $b.Bottom }
}
$width = $right - $left
$height = $bottom - $top
$bmp = New-Object System.Drawing.Bitmap($width, $height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$src = [System.Drawing.Point]::new($left, $top)
$size = [System.Drawing.Size]::new($width, $height)
$g.CopyFromScreen($src, [System.Drawing.Point]::Empty, $size)
$openclaw_media = $env:OPENCLAW_MEDIA_DIR
if (-not $openclaw_media) {
  $openclaw_media = Join-Path $env:USERPROFILE ".openclaw\media"
}
if (!(Test-Path $openclaw_media)) { New-Item -ItemType Directory -Path $openclaw_media -Force | Out-Null }
$path = Join-Path $openclaw_media ("screenshot_all_$(Get-Date -Format 'yyyyMMdd_HHmmss').png")
$bmp.Save($path)
$g.Dispose()
$bmp.Dispose()
Write-Output "MEDIA:$path"
