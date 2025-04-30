import PropTypes from "prop-types";
import { useState, useEffect, useContext } from "react";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import Form from "../components/Form";
import FormInput from "../components/FormInput";
import FormButton from "../components/FormButton.jsx";
import { AuthContext } from "../contexts"
import api from "../api/api";
import { useChatMembers, useAccount } from "../queries";

function Error({ message }) {
  return <p className="text-amber-800 text-sm">{message}</p>;
}

Error.propTypes = {
  message: PropTypes.string,
};

export default function NewMessage({chatId}) {
  const { headers, token } = useContext(AuthContext);
  const { data: fetchedAccount, isSuccess } = useAccount();
  const { members, error: memberError } = useChatMembers(chatId);
  const [disabled, setDisabled] = useState(false);
  const [messageText, setMessageText] = useState("");
  const [isMember, setIsMember] = useState(false);
  const [accountId, setAccountId] = useState(null);
    const [errorMsg, setErrorMsg] = useState("");

  
  useEffect(() => {
    if (isSuccess && fetchedAccount) {
      setAccountId(fetchedAccount.id);
    
      if (members) {
        setIsMember(members.some((member) => member.id === fetchedAccount.id));
      }
    }

  }, [isSuccess, fetchedAccount, members]);


  const mutation = useMutation({
      mutationFn: ({messageText, accountId}) => 
        api.post(`/chats/${chatId}/messages`, {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
            ...headers,
        }, { text: messageText, account_id: accountId }),
      onSuccess: () => setMessageText(""),
      onError: (error) => {
        setDisabled(false);
        setErrorMsg(error.message);
      },
    });

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate({messageText, accountId});
  }

    const sendDisabled = !messageText || disabled;

  if (isMember) {
    return (
        <form className="flex flex-row" onSubmit={handleSubmit}>
            {errorMsg && <Error message={errorMsg} />}
            <FormInput
                id="message"
                type="text"
                name="message"
                text="New Message"
                value={messageText}
                setValue={setMessageText}
            />

            <FormButton
                text="Send"
                disabled={sendDisabled}
                
            />
        </form>
    )
    }

}