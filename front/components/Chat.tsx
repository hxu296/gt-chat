import { useEffect, useState } from "react";
import { type Message, ChatLine, LoadingChatLine } from "./ChatLine";
import { useCookies } from "react-cookie";

const COOKIE_NAME = "buzz-ai-cookie";

// default first message to display in UI (not necessary to define the prompt)
export const initialMessages: Message[] = [
  {
    who: "bot",
    message:
      "Hi, I'am Buzz AI, an Q&A bot. I've read 14842 official GaTech websites from housing, cc, cse, omscs, and 20 more sub-domains. Ask me anything about Tech!\n\nExample:\nList professors doing MLSys & HPC research.\nWhat's the Co-op policy for grad students?\nWhat are ways to apply for GTA?\nWrite two creative verses about yourself, in the musical Hamilton's style.",
  },
];

const InputMessage = ({ input, setInput, sendMessage }: any) => {
  return (
    <div className="flex w-full justify-start">
      <textarea
        className="h-28 w-full resize-none rounded-md border-gray-300 hover:border-gray-400"
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            sendMessage(input);
            setInput("");
          }
        }}
        onInput={(e) => {
          e.preventDefault();
          let target = e.target as HTMLTextAreaElement;
          setInput(target.value);
        }}
        value={input}
        placeholder="Where and when can I swim?"
      ></textarea>
      <button
        className="relative -left-10"
        onClick={(e) => {
          e.preventDefault();
          sendMessage(input);
          setInput("");
        }}
      >
        <svg
          width="24"
          height="24"
          viewBox="0 0 32 32"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <title>Send</title>
          <path
            fillRule="evenodd"
            d="M5.64161 2.18531C6.04591 2.14469 6.453 2.22818 6.80868 2.42468L6.81379 2.4275L27.9217 14.25L27.9244 14.2515C28.2358 14.4244 28.4954 14.6774 28.6764 14.9842C28.8578 15.292 28.9535 15.6427 28.9535 16C28.9535 16.3572 28.8578 16.708 28.6764 17.0157C28.4954 17.3226 28.2358 17.5756 27.9244 17.7485L27.9217 17.75L6.80869 29.5753C6.45301 29.7718 6.04591 29.8553 5.64161 29.8147C5.2373 29.774 4.85495 29.6112 4.54548 29.3479C4.236 29.0846 4.01408 28.7332 3.90925 28.3406C3.80455 27.9485 3.82162 27.5338 3.95818 27.1517L7.93379 16L3.95868 4.84968C3.82192 4.46735 3.8045 4.05166 3.90925 3.65933C4.01408 3.26675 4.236 2.9154 4.54548 2.65208C4.85496 2.38875 5.2373 2.22594 5.64161 2.18531ZM27.4376 15.125L26.9489 15.9975L5.84155 4.17529L5.84205 4.17668L9.8113 15.3106C9.98396 15.7539 9.98396 16.246 9.8113 16.6894L5.84155 27.8247L26.9489 16.0025L26.9535 16L27.4376 15.125Z"
            fill="currentColor"
          ></path>
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M8 16C8 15.4477 8.44772 15 9 15H17C17.5523 15 18 15.4477 18 16C18 16.5523 17.5523 17 17 17H9C8.44772 17 8 16.5523 8 16Z"
            fill="currentColor"
          ></path>
        </svg>
      </button>
    </div>
  );
};

export function Chat() {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [cookie, setCookie] = useCookies([COOKIE_NAME]);

  useEffect(() => {
    if (!cookie[COOKIE_NAME]) {
      // generate a semi random short id
      const randomId = Math.random().toString(36).substring(7);
      setCookie(COOKIE_NAME, randomId);
    }
  }, [cookie, setCookie]);

  // send message to API /api/chat endpoint
  const sendMessage = async (message: string) => {
    setLoading(true);
    const newMessages = [
      ...messages,
      { message: message, who: "user" } as Message,
    ];
    setMessages(newMessages);

    const last10messages = newMessages.slice(-10);

    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: last10messages[last10messages.length - 1].message,
        user: cookie[COOKIE_NAME],
      }),
    });
    let botNewMessage = "";
    if (response.status != 200) {
      botNewMessage = "Failed to fetch data.";
    }

    const data = await response.json();
    if (data.text == null) {
      botNewMessage = "Failed to get answer.";
    }
    // strip out white spaces from the bot message
    botNewMessage = data.text.trim();

    setMessages([
      ...newMessages,
      { message: botNewMessage, who: "bot" } as Message,
    ]);
    setLoading(false);
  };

  return (
    <div className="flex h-full  w-8/12 flex-col justify-between rounded-2xl bg-gray-100 lg:p-6">
      <div>
        {messages.map(({ message, who }, index) => (
          <ChatLine key={index} who={who} message={message} />
        ))}

        {loading && <LoadingChatLine />}
      </div>
      <InputMessage
        input={input}
        setInput={setInput}
        sendMessage={sendMessage}
      />
    </div>
  );
}
