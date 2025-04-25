import { useChats } from ".././queries"

const navHeaders = "text-gray-400 text-xl text-bold list-none px-2"

export default function Nav() {
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