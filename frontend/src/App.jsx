import { BrowserRouter, Routes, Route, NavLink, useParams, Link } from "react-router";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import PropTypes from "prop-types";
import { useChatMessages, useChats, useUsername } from "./queries";
import AuthProvider from "./providers/AuthProvider";
import Login from "./accounts/Login"
import { useContext } from "react";
import { AuthContext } from "./contexts";
//import Nav from "./components/Nav"

const headerClassName = "text-center text-4xl font-extrabold py-4";

const queryClient = new QueryClient();

const navItems = "px-4 py-2 list-none"

const navHeaders = "text-gray-400 text-xl text-bold list-none px-2"


function NotFound() {
  return <h1 className={headerClassName}>404: Not Found</h1>;
}

function Home() {
  const { loggedIn } = useContext(AuthContext);
  const [redirect, setRedirect] = useState(false);

  useEffect(() => {
    if (loggedIn) {
      setRedirect(true);
    }
  }, [loggedIn]);

  if (redirect) {
    return <Navigate to="/chats" replace />;
  }

  return (
    <div>
      <h1 className={headerClassName}>Pony Express</h1>
      <Login />
    </div>
  );
}

function Register() {
  return <h1 className={headerClassName}>Pony Express</h1>;
}

function Settings() {
  return <h1 className={headerClassName}>Pony Express</h1>;
}

function Chats() {
  return (
    <div className="w-1/4">
      <Nav />
    </div>
  );
}

function Chat() {
  const {chatId} = useParams();
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

  return (
    <ul className="max-h-150 overflow-y-scroll">
      {messages.map((message) => (
        <Message key={message.id} text={message.text} account_id={message.account_id} created_at={message.created_at}/>
      ))}
    </ul>
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
    const getClassName = ({isActive}) =>
      isActive ? "text-orange-600" : "text-blue-500 hover:text-blue-200"
  
    return (
      <nav className="min-w-full min-h-full bg-gray-700">
        <h1 className="text-gray-300 text-2xl text-bold text-center list-none">
            Pony Express
          </h1>
        <ul>
          <li className={navHeaders}>Account</li>
          <li className={navItems}><NavLink className={getClassName} to="/settings">Settings</NavLink></li>
          <li className={navItems}><Button /></li>
          <li className={navHeaders}>Chats</li>
          {chats.map((chat) => (
            <ChatItem key={chat.id} getClassName={getClassName} {...chat}/>
          ))}
        </ul>
      </nav>
    );
}

function Button() {
    const getClassName = "hover:bg-blue-200 rounded px-2 py-1 hover:text-gray-700 text-gray-200 bg-blue-700";
    const { logout } = useContext(AuthContext);
    
    return (
        <Link to="/">
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
