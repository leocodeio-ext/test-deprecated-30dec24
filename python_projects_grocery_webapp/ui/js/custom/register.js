document.getElementById("registerForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    const formData = {
        username: document.getElementById("customer_name").value,
        password: password,
        role: document.getElementById("role").value
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData),
        });

        const result = await response.json();
        
        if (response.ok) {
            alert("Registration successful!");
            window.location.href = "login.html";
        } else {
            alert(result.message || "Registration failed");
        }
    } catch (error) {
        alert("Error during registration. Please try again.");
    }
}); 