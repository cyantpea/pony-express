import PropTypes from "prop-types";
import { useState, useEffect, useContext } from "react";
import { useMutation } from "@tanstack/react-query";
import Form from "../components/Form";
import FormInput from "../components/FormInput";
import FormButton from "../components/FormButton.jsx";
import api from "../api/api";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts.js";

const headerClassName = "text-center text-4xl font-extrabold py-4";


function Error({ message }) {
  return <p className="text-amber-800 text-sm">{message}</p>;
}

Error.propTypes = {
  message: PropTypes.string,
};

export default function Register() {
  const { loggedIn, login } = useContext(AuthContext);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirm_password, setConfirmPassword] = useState("");
  const [email, setEmail] = useState("");
  const [disabled, setDisabled] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const navigate = useNavigate();

  const mutation = useMutation({
    mutationFn: () =>
      api.form("/auth/registration", {}, { username, email, password }),
    onMutate: () => setDisabled(true),
    onSuccess: async () => {
      try {
        const data = await api.form("/auth/token", {}, { username, password });
        login(data.access_token);
      } catch (err) {
        setErrorMsg("registered, but failed to log in.");
      }
    },
    onError: (error) => {
      setDisabled(false);
      setErrorMsg(error.message);
    },
  });
  

  useEffect(() => {
    if (loggedIn) {
      navigate("/chats");
    }
  }, [loggedIn, navigate]);

  useEffect(() => {
    if (password && confirm_password && password !== confirm_password) {
      setErrorMsg("passwords do not match");
    } else {
      setErrorMsg(""); 
    }
  }, [password, confirm_password]);

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate();
  };

  const buttonDisabled = !username || !email || !password || disabled || password !== confirm_password;

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
            id="email"
            type="email"
            name="email"
            text="email"
            value={email}
            setValue={setEmail}
        />
        <FormInput
            id="password"
            type="password"
            name="password"
            text="password"
            value={password}
            setValue={setPassword}
        />
        <FormInput
            id="confirm_password"
            type="password"
            name="confirm password"
            text="confirm password"
            value={confirm_password}
            setValue={setConfirmPassword}
        />
        {errorMsg && <Error message={errorMsg} />}
        <FormButton text="register" disabled={buttonDisabled} />
        </Form>
        <p className="text-center text-sm">
            <a href="/login" className="text-blue-500 hover:underline">
            login to account
            </a>
        </p>
    </div>
  );
}
