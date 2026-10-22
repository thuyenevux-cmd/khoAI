
$ErrorActionPreference = "Stop"
$docxPath = "D:\it-thesis-research-documentation-engineer-v3.0\report\Word\Bao_cao_AIA331.docx"
$pdfPath = "D:\it-thesis-research-documentation-engineer-v3.0\report\Word\Bao_cao_AIA331.pdf"

$word = $null
$doc = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $doc = $word.Documents.Open($docxPath, $false, $true)
    $doc.SaveAs2($pdfPath, 17)
    Write-Host "XUAT_PDF_THANH_CONG"
} catch {
    Write-Error "Loi xuat PDF: $_"
} finally {
    if ($doc -ne $null) {
        $doc.Close($false)
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($doc)
    }
    if ($word -ne $null) {
        $word.Quit()
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($word)
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
