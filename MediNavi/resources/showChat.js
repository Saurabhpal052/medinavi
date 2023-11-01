function toggleChatBox() {
    var element = document.getElementById("chatbox");
    
    if (element.style.display === "none") {
        element.style.display = "block";  // Show the element
    } else {
        element.style.display = "none";   // Hide the element
    }
}