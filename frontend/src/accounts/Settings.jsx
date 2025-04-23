import PropTypes from "prop-types";
import { useState, useEffect, useContext } from "react";
import { useMutation } from "@tanstack/react-query";
import { Navigate } from "react-router";
import Form from "../components/Form";
import FormInput from "../components/FormInput";
import FormButton from "../components/FormButton.jsx";
import { useAuth } from "../hooks";
import api from "../api/api";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

const headerClassName = "text-center text-4xl font-extrabold py-4";


function Error({ message }) {
  return <p className="text-amber-800 text-sm">{message}</p>;
}

Error.propTypes = {
  message: PropTypes.string,
};

export default function Settings() {
  const [username, setUsername] = useState("");
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");
  const [email, setEmail] = useState("");
  const [accountDisabled, setAccountButtonDisabled] = useState(false);
  const [passwordDisabled, setPasswordButtonDisabled] = useState(false);
  const [passwordErrorMsg, setPasswordErrorMsg] = useState("");
  const [accountErrorMsg, setAccountErrorMsg] = useState("");
  const [deleteErrorMsg, setDeleteErrorMsg] = useState("");
  const {token, logout} = useAuth();

  useEffect(() => {
    async function fetchUserInfo() {
      try {
        const data = await api.get("/accounts/me", {
        Authorization: `Bearer ${token}`,
      });
        setUsername(data.username);
        setEmail(data.email);
      } catch (error) {
        setAccountErrorMsg("Failed to fetch user info: " + error.message);
      }
    }
  
    fetchUserInfo();
  }, []);

  const deleteMutation = useMutation({
    mutationFn: () =>  
        api._delete("/accounts/me/", {
        Authorization: `Bearer ${token}`,
      }),
    onSuccess: () => {
      logout();
    },
    onError: (error) => {
        setDeleteErrorMsg(error.message);
    },
  });
  
  const accountMutation = useMutation({
    mutationFn: () =>
      api.putForm("/accounts/me/", {
        Authorization: `Bearer ${token}`,
      }, { username, email }),
    onMutate: () => setAccountButtonDisabled(true),
    onSuccess: () => {
      setAccountButtonDisabled(false);
    },
    onError: (error) => {
      setAccountButtonDisabled(false);
      setAccountErrorMsg(error.message);
    },
  });

    const passwordMutation = useMutation({ 
    mutationFn: () =>
      api.putForm("/accounts/me/password/", {
        Authorization: `Bearer ${token}`,
      }, { oldPassword, newPassword }),
    onMutate: () => setPasswordButtonDisabled(true),
    onSuccess: async () => {
      setPasswordButtonDisabled(false);
      setOldPassword("");
      setNewPassword("");
      setConfirmNewPassword("");
    },
    onError: (error) => {
      setPasswordButtonDisabled(false);
      setPasswordErrorMsg(error.message);
    }
    });
  


  useEffect(() => {
    if (newPassword && confirmNewPassword && newPassword !== confirmNewPassword) {
      setPasswordErrorMsg("passwords do not match");
    } else {
      setPasswordErrorMsg(""); 
    }
  }, [newPassword, confirmNewPassword]);

  const accountHandleSubmit = (e) => {
    e.preventDefault();
    accountMutation.mutate();
  };

  const handlePasswordSubmit = (e) => {
    e.preventDefault();
    passwordMutation.mutate();
  }

  const accountButtonDisabled = !username || !email || accountDisabled;
  const passwordButtonDisabled = !oldPassword || !newPassword || !confirmNewPassword || passwordDisabled || newPassword !== confirmNewPassword;
  return (
    <div className="max-h-175 overflow-y-scroll">
      <h1 className={headerClassName}>Settings</h1>
      <h2 className="text-center text-2xl font-bold py-2">Update your account</h2>
        <Form onSubmit={accountHandleSubmit}>
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
        {accountErrorMsg && <Error message={accountErrorMsg} />}
        <FormButton text="update" disabled={accountButtonDisabled} />
        
      </Form>
      <h2 className="text-center text-2xl font-bold py-2">Update your password</h2>
        <Form onSubmit={handlePasswordSubmit}>
        <FormInput
            id="oldPassword"
            type="password"
            name="old password"
            text="old password"
            value={oldPassword}
            setValue={setOldPassword}
        />
        <FormInput
            id="newPassword"
            type="password"
            name="new password"
            text="new password"
            value={newPassword}
            setValue={setNewPassword}
        />
        <FormInput
            id="confirmNewPassword"
            type="password"
            name="confirm new password"
            text="confirm new password"
            value={confirmNewPassword}
            setValue={setConfirmNewPassword}
        />
        {passwordErrorMsg && <Error message={passwordErrorMsg} />}
        <FormButton text="update password" disabled={passwordButtonDisabled} />
        </Form>
        <h2 className="text-center text-2xl font-bold py-2">Manage account</h2>
        <Link to="/">
            <button onClick={logout()} type="button" className="hover:bg-blue-200 rounded px-2 py-1 hover:text-gray-700 text-gray-200 bg-blue-700">Logout</button>
        </Link>
        <Link to="/">
            <button onClick={logout()} type="button" className="hover:bg-red-200 rounded px-2 py-1 hover:text-gray-700 text-gray-200 bg-red-700">Delete</button>
        </Link>
    </div>
  );
}
