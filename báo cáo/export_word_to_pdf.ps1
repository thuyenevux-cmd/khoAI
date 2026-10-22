$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$docxPath = Join-Path $scriptDir "Bao_cao_AIA331.docx"
$pdfPath = Join-Path $scriptDir "báo cáo dự án Kho AI nhóm 11.pdf"
$copyPdfPath = Join-Path $scriptDir "Bao_cao_AIA331.pdf"

Write-Host "Opening DOCX: $docxPath"

$word = $null
$doc = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = [Microsoft.Office.Interop.Word.WdAlertLevel]::wdAlertsNone
    $doc = $word.Documents.Open($docxPath, $false, $true)
    Write-Host "DOCX opened successfully. Exporting to: $pdfPath"
    $doc.ExportAsFixedFormat($pdfPath, 17) # 17 = wdExportFormatPDF
    Write-Host "XUAT_PDF_MASTER_THANH_CONG: $pdfPath"
    Copy-Item -Path $pdfPath -Destination $copyPdfPath -Force
    Write-Host "XUAT_PDF_COPY_THANH_CONG: $copyPdfPath"
} catch {
    Write-Error "Loi xuat PDF: $_"
} finally {
    if ($doc -ne $null) {
        try { $doc.Close([Microsoft.Office.Interop.Word.WdSaveOptions]::wdDoNotSaveChanges) } catch {}
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($doc)
    }
    if ($word -ne $null) {
        try { $word.Quit() } catch {}
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($word)
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
