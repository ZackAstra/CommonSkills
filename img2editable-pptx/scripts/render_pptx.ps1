param([string]$pptx, [string]$png)
$app = New-Object -ComObject PowerPoint.Application
$pres = $app.Presentations.Open($pptx, $true, $false, $false)
$slide = $pres.Slides.Item(1)
$slide.Export($png, "PNG", 1640, 810)
$pres.Close()
$app.Quit()
Write-Output "exported"
