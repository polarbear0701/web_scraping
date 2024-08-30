document.getElementById('downloadBtn').addEventListener('click', function() {
    // Get the selected file name from the dropdown
    const selectedFile = document.getElementById('csvSelect').value;
    // Redirect to the download route with the selected file name as a query parameter
    window.location.href = '/download?file_name=' + selectedFile;
});
