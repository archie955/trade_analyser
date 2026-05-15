const getUser = () => {
  const token = window.localStorage.getItem("JSONUser");
  const username = window.localStorage.getItem("username");

  if (!token || !username) {
    return null;
  }

  return { username: username, token: token };
};

const saveUser = (user) => {
  window.localStorage.setItem("JSONUser", user.token);
  window.localStorage.setItem("username", user.username);
};

const removeUser = () => {
  window.localStorage.removeItem("JSONUser");
  window.localStorage.removeItem("username");
};

export default { getUser, saveUser, removeUser };
