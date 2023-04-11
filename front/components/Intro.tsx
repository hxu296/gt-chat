import Balancer from "react-wrap-balancer";
import { motion } from "framer-motion";
import { FADE_DOWN_ANIMATION_VARIANTS } from "@/lib/constants";
import GitHub from "@/components/icons/github";

export function Intro() {
  return (
    <div className="mt-1">
      <motion.h1
        className="w-[1024px] bg-gradient-to-br from-black to-stone-500 bg-clip-text text-center text-4xl font-bold tracking-[-0.02em] drop-shadow-sm md:text-4xl md:leading-[5rem]"
        variants={FADE_DOWN_ANIMATION_VARIANTS}
      >
        <Balancer>
          <span>Buzz AI -- </span>
          <span>24/7 GT advisor for&nbsp;</span>
          <span className="bg-co bg-gradient-to-r from-blue-500 via-green-600 to-indigo-500 bg-clip-text text-transparent">
            anything
          </span>
        </Balancer>
      </motion.h1>
      <a
        href="https://github.com/hxu296/gt-chat"
        target="_blank"
        rel="noreferrer"
        className="mx-auto mb-3 flex max-w-fit items-center justify-center space-x-2 overflow-hidden rounded-full border border-black bg-white px-5 py-2 text-black transition-colors hover:bg-black hover:text-white"
      >
        <GitHub className="h-5 w-5" />
        <p className="text-sm font-semibold">Star on GitHub</p>
      </a>
    </div>
  );
}
