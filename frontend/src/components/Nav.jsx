import { useChats } from ".././queries"

const navHeaders = "text-gray-400 text-xl text-bold list-none px-2"

export default function Nav() {
    const { chats } = useChats();
    const getClassName = ({isActive}) =>
      isActive ? "text-orange-600" : "text-blue-500 hover:text-blue-200"
  
    return (
      <nav className="min-w-full min-h-full bg-gray-700">
        <ul>
          <li className="text-gray-400 text-2xl text-bold text-center list-none">
            Pony Express
          </li>
          <li className={navHeaders}>Account</li>
          <li className={navItems}><NavLink to="/settings">Settings</NavLink></li>
          <Button />
          <li className={navHeaders}>Chats</li>
          {chats.map((chat) => (
            <ChatItem key={chat.id} getClassName={getClassName} {...chat}/>
          ))}
        </ul>
      </nav>
    );
}

function Button() {
    const className =
    "border border-violet-800 rounded px-4 py-2 text-center" +
    (disabled ? " bg-gray-400 italic" : " hover:bg-lime-600 cursor-pointer");

    return (
        <Link to="/home">
            <button type="button" className={className}>Logout</button>
        </Link>
    );
}