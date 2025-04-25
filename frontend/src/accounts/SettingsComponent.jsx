import PropTypes from "prop-types";
import { useState, useEffect, useContext } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import Form from "../components/Form.jsx";
import FormInput from "../components/FormInput.jsx";
import FormButton from "../components/FormButton.jsx";
import { AuthContext } from "../contexts.js";
import api from "../api/api.js";
import { Link, useNavigate } from "react-router-dom";
import { useAccount } from "../queries";

const headerClassName = "text-center text-4xl font-extrabold py-4";


function Error({ message }) {
  return <p className="text-amber-800 text-sm">{message}</p>;
}

Error.propTypes = {
  message: PropTypes.string,
};

export default function SettingsComponent() {
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");
  const [accountDisabled, setAccountButtonDisabled] = useState(false);
  const [passwordDisabled, setPasswordButtonDisabled] = useState(false);
  const [passwordErrorMsg, setPasswordErrorMsg] = useState("");
  const [accountErrorMsg, setAccountErrorMsg] = useState("");
  const [deleteErrorMsg, setDeleteErrorMsg] = useState("");
  const { headers, token, logout } = useContext(AuthContext);
  const [account, setAccount] = useState({ username: "", email: "" });
  const { data: fetchedAccount, isSuccess } = useAccount();
  const navigate = useNavigate();

  useEffect(() => {
    if (isSuccess && fetchedAccount) {
      setAccount({
        username: fetchedAccount.username,
        email: fetchedAccount.email,
      });
    }
  }, [isSuccess, fetchedAccount]);

  const deleteMutation = useMutation({
    mutationFn: () =>  
        api._delete("/accounts/me/", {
        Authorization: `Bearer ${token}`,
        ...headers,
      }),
    onSuccess: () => {
      logout();
      navigate("/")
    },
    onError: (error) => {
        setDeleteErrorMsg(error.message);
    },
  });
  
  const accountMutation = useMutation({
    mutationFn: (account) => 
      api.put("/accounts/me/", {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        ...headers,
      }, {username: account.username, email: account.email}),
    onMutate: () => setAccountButtonDisabled(true),
    onSuccess: () => {
      setAccountButtonDisabled(false);
      setAccountErrorMsg("");
    },
    onError: (error) => {
      setAccountButtonDisabled(false);
      setAccountErrorMsg(error.message);
    },
  });

    const passwordMutation = useMutation({ 
    mutationFn: ({oldPassword, newPassword}) =>
      api.putForm("/accounts/me/password/", {
        Authorization: `Bearer ${token}`,
        ...headers,
      }, { old_password: oldPassword, new_password: newPassword }),
    onMutate: () => setPasswordButtonDisabled(true),
    onSuccess: async () => {
      setPasswordButtonDisabled(false);
      setOldPassword("");
      setNewPassword("");
      setConfirmNewPassword("");
      setPasswordErrorMsg("");
    },
    onError: (error) => {
      setPasswordButtonDisabled(false);
      if (error.status === 401) 
        setPasswordErrorMsg("old password is incorrect");
      else 
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
    accountMutation.mutate(account);
  };

  const handlePasswordSubmit = (e) => {
    e.preventDefault();
    passwordMutation.mutate({oldPassword, newPassword});
  }

  const accountButtonDisabled = !account.username || !account.email || accountDisabled;
  const passwordButtonDisabled = !oldPassword || !newPassword || !confirmNewPassword || passwordDisabled || newPassword !== confirmNewPassword;
  return (
    <div className="max-h-160 min-h-full overflow-y-scroll">
      <h1 className={headerClassName}>Settings</h1>
      <h2 className="text-center text-2xl font-bold py-2">Update your account</h2>
        <Form onSubmit={accountHandleSubmit}>
        <FormInput
            id="username"
            type="text"
            name="username"
            text="username"
            value={account.username}
            setValue={(value) => setAccount((prev) => ({ ...prev, username: value }))}
        />
        <FormInput
            id="email"
            type="email"
            name="email"
            text="email"
            value={account.email}
            setValue={(value) => setAccount((prev) => ({ ...prev, email: value }))}
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
        <div className="flex justify-center gap-8">
          <Link to="/">
              <button onClick={logout} type="button" className="hover:bg-blue-700 rounded px-2 py-1 hover:text-gray-200 text-gray-700 bg-blue-200 border border-blue-700">Logout</button>
          </Link>
          {deleteErrorMsg && <Error message={deleteErrorMsg} />}
          <Link to="/">
              <button onClick={() => deleteMutation.mutate()} type="button" className="hover:bg-red-700 rounded px-2 py-1 hover:text-gray-200 text-red-700 bg-red-200 border border-red-700">Delete</button>
          </Link>
        </div>
    </div>
  );
}
