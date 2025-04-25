import { BrowserRouter, Routes, Route, NavLink, useParams, Link, useNavigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import PropTypes from "prop-types";
import { useChatMessages, useChats, useUsername } from "./queries";
import AuthProvider from "./providers/AuthProvider";
import Login from "./accounts/Login"
import { useContext } from "react";
import { AuthContext } from "./contexts";
import { useEffect, useState, useRef } from "react";
import Register from "./accounts/Registration"
import NewMessage from "./components/NewMessage";
import SettingsComponent from "./accounts/SettingsComponent"
import { useLoggedOut } from "./hooks";
import { useAccount } from "./queries";

const headerClassName = "text-center text-4xl font-extrabold py-4";

const queryClient = new QueryClient();

const navItems = "px-4 py-2 list-none"

const navHeaders = "text-gray-400 text-xl text-bold list-none px-2"


function NotFound() {
  return <h1 className={headerClassName}>404: Not Found</h1>;
}

function Home() {
  const { loggedIn } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (loggedIn) {
      navigate("/chats");
    }
  }, [loggedIn, navigate]);

  return (
    <div>
      <Login />
    </div>
  );
}

function Settings() {
  useLoggedOut();
  return (
    <div className="flex">
      <div className="w-1/4">
        <Nav />
      </div>
      <div className="w-3/4 p-4">
        <SettingsComponent />
      </div>
    </div>
  )
}

function Chats() {
  useLoggedOut();
  return (
    <div className="w-1/4">
      <Nav />
    </div>
  );
}

function Chat() {
  const {chatId} = useParams();
  useLoggedOut();
  return (
    <div className="flex">
      <div className="w-1/4">
        <Nav />
      </div>
      <div className="w-3/4 p-4">
        <Messages chatId={chatId}/>
      </div>
    </div>
  );
}


function ChatItem({id, name, getClassName}) {
  return (
    <li className={navItems}>
      <NavLink to={`/chats/${id}`} className={getClassName}>
        {name}
      </NavLink>
    </li>
  );

}

ChatItem.propTypes = {
  id: PropTypes.number,
  name: PropTypes.string,
  getClassName: PropTypes.func,
};


function Messages({chatId}) {
  const { messages } = useChatMessages(chatId);
  const [scrollValue, setScrollValue] = useState(0);
  const listRef = useRef(null);

  useEffect(() => {
      // update scrollValue anytime listRef.current is scrolled
      listRef.current.addEventListener("scroll", () => {
        setScrollValue(Math.round(listRef.current.scrollTop));
      });
    }, []);

  const scrollToBottom = () => {
    listRef.current.scrollTo({
      top: listRef.current.scrollHeight,
      left: 0,
      behavior: "smooth",
    });
  };

  useEffect(() => {
    if (listRef.current) {
      scrollToBottom();
    }
  }, [messages]);

  return (
    <div className="flex flex-row justify-between">
    <ul ref={listRef} className="h-[calc(100lvh-256px)] max-h-160 min-h-full overflow-y-scroll">
      {messages.map((message) => (
        <Message key={message.id} text={message.text} account_id={message.account_id} created_at={message.created_at}/>
      ))}
    </ul>
    <NewMessage chatId={chatId} />
    </div>
  );
}

Messages.propTypes = {
  chatId: PropTypes.string,
};

function Message({ text, account_id,  created_at }) {
  const { username } = useUsername(account_id);
  const date = new Date(created_at);

  return (
    <li className="p-2 bg-gray-200 m-2 rounded-sm">
      <div className="flex justify-between text-gray-400">
        <span>{username}</span> 
        <span>{date.toLocaleString()}</span>
      </div>
      <div className="py-2">
        {text}
      </div>
    </li>
  );
}

Message.propTypes = {
  text: PropTypes.string,
  account_id: PropTypes.number,
  created_at: PropTypes.string
};

function Nav() {
    const { chats } = useChats();
      const [username, setUsername] = useState("");
      const { data: fetchedAccount, isSuccess } = useAccount();
    
      useEffect(() => {
        if (isSuccess && fetchedAccount) {
          setUsername(fetchedAccount.username);
        }
      }, [isSuccess, fetchedAccount]);
    
    const getClassName = ({isActive}) =>
      isActive ? "text-orange-600" : "text-blue-500 hover:text-blue-200"
  
    return (
      <nav className="min-w-full min-h-full bg-gray-700">
        <h1 className="text-gray-300 text-2xl text-bold text-center list-none">
            Pony Express
          </h1>
        <ul>
          <li className={navHeaders}>{username}</li>
          <li className={navItems}><NavLink className={getClassName} to="/settings">Settings</NavLink></li>
          <li className={navItems}><LogoutButton /></li>
          <li className={navHeaders}>Chats</li>
          {chats.map((chat) => (
            <ChatItem key={chat.id} getClassName={getClassName} {...chat}/>
          ))}
        </ul>
      </nav>
    );
}

function LogoutButton() {
    const getClassName = "hover:bg-blue-200 rounded px-2 py-1 hover:text-gray-700 text-gray-200 bg-blue-700";
    const { logout } = useContext(AuthContext);
    
    return (
        <Link to="/login">
            <button onClick={logout} type="button" className={getClassName}>Logout</button>
        </Link>
    );
}



function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/chats" element={<Chats />} />
            <Route path="/chats/:chatId" element={<Chat />} />
            <Route path="*" element={<NotFound />} />
            <Route path="/login" element={<Login/>} />
            <Route path="/register" element={<Register/>} />
            <Route path="/settings" element={<Settings/>} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
