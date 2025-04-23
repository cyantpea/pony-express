import PropTypes from "prop-types";
import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Navigate } from "react-router";
import Form from "../components/Form";
import FormInput from "../components/FormInput";
import FormButton from "../components/FormButton.jsx";
import { useAuth } from "../hooks";
import api from "../api/api";

const headerClassName = "text-center text-4xl font-extrabold py-4";


function Error({ message }) {
  return <p className="text-amber-800 text-sm">{message}</p>;
}

Error.propTypes = {
  message: PropTypes.string,
};

export default function Login() {
  const { loggedIn, login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [disabled, setDisabled] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const mutation = useMutation({
    mutationFn: () => api.form("/auth/token", {}, { username, password }),
    onMutate: () => setDisabled(true),
    onSuccess: (data) => login(data.access_token),
    onError: (error) => {
      setDisabled(false);
      setErrorMsg(error.message);
    },
  });

  if (loggedIn) {
    return <Navigate to="/chats" />;
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate();
  };

  const buttonDisabled = !username || !password || disabled;

  return (
    <div>
      <h1 className={headerClassName}>Pony Express</h1>
      <Form onSubmit={handleSubmit}>
        <FormInput
          id="username"
          type="text"
          name="username"
          text="username"
          value={username}
          setValue={setUsername}
        />
        <FormInput
          id="password"
          type="password"
          name="password"
          text="password"
          value={password}
          setValue={setPassword}
        />
        {errorMsg && <Error message={errorMsg} />}
        <FormButton text="login" disabled={buttonDisabled} />
      </Form>
      <p className="text-center text-sm">
        <a href="/register" className="text-blue-500 hover:underline">
          register new account
        </a>
      </p>
    </div>
      
  );
}
