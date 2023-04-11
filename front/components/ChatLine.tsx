import Balancer from "react-wrap-balancer";

const BalancerWrapper = (props: any) => <Balancer {...props} />;

export type Message = {
  who: "bot" | "user" | undefined;
  message?: string;
};

// loading placeholder animation for the chat line
export const LoadingChatLine = () => (
  <div className="flex min-w-full animate-pulse px-4 py-5 sm:px-6">
    <div className="flex flex-grow space-x-3">
      <div className="min-w-0 flex-1">
        <p className="font-large text-xxl text-gray-900">
          <a href="#" className="hover:underline">
            Buzz AI
          </a>
        </p>
        <div className="space-y-4 pt-4">
          <div className="grid grid-cols-3 gap-4">
            <div className="col-span-2 h-2 rounded bg-zinc-500"></div>
            <div className="col-span-1 h-2 rounded bg-zinc-500"></div>
          </div>
          <div className="h-2 rounded bg-zinc-500"></div>
        </div>
      </div>
    </div>
  </div>
);

// util helper to convert new lines to <br /> tags
const convertNewLines = (text: string) =>
  text.split("\n").map((line, i) => (
    <span key={i}>
      {line}
      <br />
    </span>
  ));

function extractSources(text: string): {
  content: string;
  urls: Array<string>;
} {
  const urlPattern =
    /http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+/g;
  const split = text.split("SOURCES:");

  const urls = ((split.length > 1 && split[1].match(urlPattern)) || []).map(
    (url) => url.replace(",", ""),
  );
  const hasUrls = urls && urls.length > 0;

  const content = hasUrls ? split[0].trim() : text.trim();

  return {
    content,
    urls: removeDuplicates(urls),
  };
}

function removeDuplicates<T>(array: T[]): T[] {
  return [...new Set(array)];
}

function formatText(text: string): {
  content: Array<JSX.Element>;
  urls: Array<string>;
} {
  const { content, urls } = extractSources(text);
  return { content: convertNewLines(content), urls };
}

export function ChatLine({ who = "bot", message }: Message) {
  if (!message) {
    return null;
  }
  const { content, urls } = formatText(message);
  const cl = who == "bot" ? "font- font-semibold " : "";
  return (
    <div
      className={
        who != "bot" ? "float-right clear-both" : "float-left clear-both"
      }
    >
      {/* <BalancerWrapper> */}
      <div className="min-h-2xl text-dark-100 float-right mb-5 max-w-3xl rounded-lg bg-gray-100 px-3 py-4 ring-1 ring-zinc-300 sm:px-3">
        <div className="flex flex-col justify-between space-x-3">
          <div className="flex-1 gap-4">
            <p className={"text " + cl}>{content}</p>
            {urls && urls.length > 0 && (
              <div className="">
                <br />
                <div>Sources:</div>
                {urls.map((url, index) => (
                  <div key={url}>
                    {"> "}
                    <a href={url} className="underline">
                      {url}
                    </a>
                  </div>
                ))}
              </div>
            )}
            {who === "bot" && (
              <div className="text-sm font-thin italic">
                <br />
                <p>Warning: Not all answers are correct!</p>
              </div>
            )}
          </div>
        </div>
      </div>
      {/* </BalancerWrapper> */}
    </div>
  );
}
