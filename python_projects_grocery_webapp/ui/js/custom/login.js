document
  .getElementById("loginForm")
  .addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = {
      username: document.getElementById("customer_name").value,
      password: document.getElementById("password").value,
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (response.ok) {
        localStorage.setItem("user", JSON.stringify(result.user));
        window.location.href = "index.html";
      } else {
        alert(result.message || "Login failed");
      }
    } catch (error) {
      alert("Error during login. Please try again.");
    }
  });
