param([string]$Destino = (Get-Location).Path)
$ErrorActionPreference = 'Stop'
$Origem = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path (Join-Path $Destino 'src'))) { throw 'A pasta de destino deve conter src. Abra a raiz MESA_FARTAI_CHATBOT no VS Code.' }
$Itens = @('src','assets','tests','requirements.txt','integrantes.txt')
foreach ($item in $Itens) {
 $fonte = Join-Path $Origem $item
 if (Test-Path $fonte) {
  $alvo = Join-Path $Destino $item
  if (Test-Path $fonte -PathType Container) {
   New-Item -ItemType Directory -Force -Path $alvo | Out-Null
   Copy-Item -Path (Join-Path $fonte '*') -Destination $alvo -Recurse -Force
  } else { Copy-Item -Path $fonte -Destination $alvo -Force }
 }
}
Write-Host 'AC-4 copiada para:' $Destino
Write-Host 'Execute: python -m pip install -r requirements.txt'
Write-Host 'Execute: python -m pytest -q'
Write-Host 'Execute: python -m streamlit run src/app.py'
