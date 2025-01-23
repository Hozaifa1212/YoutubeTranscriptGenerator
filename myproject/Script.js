$.ajax({
    url: "/transcribe",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({ youtube_url: youtubeUrl, language: "bn-BD" }),
    success: function(response) {
        $("#transcription").text(response.transcription);
    },
    error: function(xhr) {
        let errorMessage = "An error occurred.";
        if (xhr.responseJSON && xhr.responseJSON.error) {
            errorMessage = xhr.responseJSON.error;
        } else if (xhr.status === 405) {
            errorMessage = "HTTP 405: Method Not Allowed. Please check the backend route and allowed methods.";
        } else {
            errorMessage = `Unexpected error: ${xhr.statusText}`;
        }
        alert(errorMessage);
    }
});

function transcribeYouTubeVideo() {
    // Get the YouTube URL from an input field with ID 'youtube-url'
    const youtubeUrl = $("#youtube-url").val(); 

    // Make an AJAX POST request to the Flask backend
    $.ajax({
        url: "/transcribe", // Backend endpoint defined in Flask
        method: "POST", // HTTP method
        contentType: "application/json", // Content type of the request
        data: JSON.stringify({ youtube_url: youtubeUrl, language: "bn-BD" }), // Data to send (YouTube URL and optional language)
        
        success: function(response) {
            // On success, display the transcription in an element with ID 'transcription'
            $("#transcription").text(response.transcription); 
        },
        error: function(xhr) {
            // Handle errors by alerting the user with the error message from the response
            alert("Error: " + xhr.responseJSON.error);
        }
    });
}
