import jsonServerProvider from "ra-data-json-server";
import { useEffect, useState } from "react";
import { useHistory } from "react-router";
import auth from "../auth/auth";

export const Home = (props) => {
  // History hook
  const history = useHistory();

  // User information hook
  const [user, setUser] = useState({
    id: "",
    email: "",
    is_active: true,
    is_superuser: false,
    firstName: "",
    lastName: "",
  });

  // Fetch user information on page load
  useEffect(() => {
    const fetchData = async () => {
      if (auth.isAuthenticated()) {
        const result = await auth.getUser();
        setUser(result);
      }
    };
    fetchData();
    // eslint-disable-next-line
  }, []);

  // Function to call logout
  const callLogout = async () => {
    auth.logout(() => {
      history.push("/");
    });
  };

  const dataProvider = jsonServerProvider("localhost:8000");

  return (
    <>
      //{" "}
      <Admin dataProvider={dataProvider}>
        // <Resource name="users" list={ListGuesser} />
        //{" "}
      </Admin>
    </>
  );
};
