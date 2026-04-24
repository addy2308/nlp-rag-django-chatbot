$(document).ready(function () {
    
    $("#question_btn").click(function (event) {
        event.preventDefault(); // Prevent default form submission
        $("#acknowledge").empty();
        
        // Get the value from the input field
        const question = $("#question").val();
        console.log("Question:", question);
        const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        // Send the file using AJAX 
        $.ajax({
            url: `/query/`,  // Current URL
            type: "POST",
            data: {
                'question': question,
                csrfmiddlewaretoken: csrfToken
            },
            success: function (response) {
                console.log("Response from server:", response.answer); // Debugging line to check the response
                $("#acknowledge").html("<div class='alert alert-success'>" + response.answer + "</div>");
            },
            error: function (xhr, status, error) {
                console.error("Error occurred:", error); // Debugging line to check for errors
                $("#acknowledge").html("<div class='alert alert-danger'>An error occurred while submitting the question.</div>");
            }
        });       
       
    });    
});