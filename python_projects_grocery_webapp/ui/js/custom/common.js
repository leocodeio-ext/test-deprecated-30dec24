function checkAuth() {
  const user = localStorage.getItem("user");
  if (!user) {
    window.location.href = "login.html";
    return false;
  }
  return true;
}
