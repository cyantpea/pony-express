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

export default function NewMessage({chatId}) {
  const [accountId, setAccountId] = useState(-1);
  const { data: fetchedAccount, isSuccess } = useAccount();
  const { members, error: memberError } = useChatMembers(chatId);
  const [disabled, setDisabled] = useState(false);
  const [messageText, setMessageText] = useState("");
  const [isMember, setIsMember] = useState(false);

  
  useEffect(() => {
    if (isSuccess && fetchedAccount) {
      setAccountId({
        id: fetchedAccount.id
      });
    }
    if (isSuccess && fetchedAccount && members) {
      setIsMember(members.some((member) => member.id === fetchedAccount.id));
    }

  }, [isSuccess, fetchedAccount, members]);


  const mutation = useMutation({
      mutationFn: () => api.post(`/chats/${chatId}/messages`, {
        Authorization: `Bearer ${token}`,
        ...headers,
      }, { messageText }),
      onMutate: () => setDisabled(true),
      onSuccess: () => setMessageText(""),
      onError: (error) => {
        setDisabled(false);
        setErrorMsg(error.message);
      },
    });

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate();
  }

    const sendDisabled = !messageText || disabled;

  if (isMember) {
    return (
        <Form onSubmit={handleSubmit}>
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
        </Form>
    )
    }

}