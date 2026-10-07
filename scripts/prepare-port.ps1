$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Temp = Join-Path $Root '.upstream-ultracraft'

if (Test-Path $Temp) { Remove-Item $Temp -Recurse -Force }

git clone --depth 1 --branch fabric-1.20.1 https://github.com/absolutelyaya/ultracraft.git $Temp

Get-ChildItem $Temp -Force | Where-Object { $_.Name -ne '.git' } | ForEach-Object {
    $dest = Join-Path $Root $_.Name
    if (Test-Path $dest -and $_.Name -notin @('port','scripts','.github','README.md','PORTING.md')) {
        Remove-Item $dest -Recurse -Force
    }
    if ($_.Name -notin @('port','scripts','.github','README.md','PORTING.md')) {
        Copy-Item $_.FullName $dest -Recurse -Force
    }
}

Copy-Item (Join-Path $Root 'port\gradle.properties') (Join-Path $Root 'gradle.properties') -Force
Copy-Item (Join-Path $Root 'port\settings.gradle') (Join-Path $Root 'settings.gradle') -Force
Copy-Item (Join-Path $Root 'port\build.gradle') (Join-Path $Root 'build.gradle') -Force
Copy-Item (Join-Path $Root 'port\fabric.mod.json') (Join-Path $Root 'src\main\resources\fabric.mod.json') -Force

Remove-Item $Temp -Recurse -Force
Write-Host 'Prepared ULTRACRAFT upstream source with the Fabric 1.21.1 port overlay.'
Write-Host 'Next: .\gradlew.bat compileJava --continue'
