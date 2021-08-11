class Auth {
  login = async (email: string, password: string) => {
    // Assert email is not empty
    if (!(email.length > 0)) {
      throw new Error("Email was not provided");
    }
    // Assert password is not empty
    if (!(password.length > 0)) {
      throw new Error("Password was not provided");
    }
    // Create data JSON
    const formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);
    // Create request
    const request = new Request("http://localhost:8000/auth/jwt/login", {
      method: "POST",
      body: formData,
    });
    // Fetch request
    const response = await fetch(request);
    // 500 error handling
    if (response.status === 500) {
      throw new Error("Internal server error");
    }
    // Extracting response data
    const data = await response.json();
    // 400 error handling
    if (response.status >= 400 && response.status < 500) {
      if (data.detail) {
        throw data.detail;
      }
      throw data;
    }
    // Successful login handling
    if ("access_token" in data) {
      localStorage.setItem("token", data["access_token"]);
      localStorage.setItem("permissions", "user");
    }
    return data;
  };

  register = async (
    firstName: string,
    lastName: string,
    email: string,
    password: string,
    passwordConfirmation: string
  ) => {
    // Assert firstName, lastName and phone not empty
    if (!(firstName.length > 0)) {
      throw new Error("First Name was not provided");
    }
    // Assert firstName, lastName and phone not empty
    if (!(lastName.length > 0)) {
      throw new Error("Last Name was not provided");
    }
    // Assert email is not empty
    if (!(email.length > 0)) {
      throw new Error("Email was not provided");
    }
    // Assert password is not empty
    if (!(password.length > 0)) {
      throw new Error("Password was not provided");
    }
    // Assert password confirmation is not empty
    if (!(passwordConfirmation.length > 0)) {
      throw new Error("Password confirmation was not provided");
    }
    // Assert email or password or password confirmation is not empty
    if (password !== passwordConfirmation) {
      throw new Error("Passwords do not match");
    }
    // Create data JSON
    const formData = {
      email: email,
      password: password,
      firstName: firstName,
      lastName: lastName,
    };
    // Create request
    const request = new Request("http://localhost:8000/auth/register", {
      method: "POST",
      body: JSON.stringify(formData),
      headers: { "Content-Type": "Application/json" },
    });
    // Fetch request
    const response = await fetch(request);
    // 500 error handling
    if (response.status === 500) {
      throw new Error("Internal server error");
    }
    // 400 error handling
    const data = await response.json();
    if (response.status >= 400 && response.status < 500) {
      if (data.detail) {
        throw data.detail;
      }
      throw data;
    }
    // Successful login handling
    if ("access_token" in data) {
      // eslint-disable-next-line
      localStorage.setItem("token", data["access_token"]);
      localStorage.setItem("permissions", "user");
    }
    return data;
  };

  logout = (callback: Function) => {
    localStorage.removeItem("token");
    localStorage.removeItem("permissions");
    // Using a callback to load '/' when logout is called
    callback();
  };

  getUser = async () => {
    const token = localStorage.getItem("token");
    // Create request
    const request = new Request("http://localhost:8000/auth/users/me", {
      method: "GET",
      headers: { Authorization: `Bearer ${token}` },
    });
    // Fetch request
    const response = await fetch(request);
    const data = await response.json();
    return data;
  };

  isAuthenticated = () => {
    const permissions = localStorage.getItem("permissions");
    if (!permissions) {
      return false;
    }
    return permissions === "user" ? true : false;
  };
}

export default new Auth();
