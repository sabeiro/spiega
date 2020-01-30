#!/usr/bin/env runhaskell
import Text.Pandoc.JSON

main :: IO ()
main = toJSONFilter inchead
  where inchead (Header n attr xs) = Header (n+1) attr xs
        inchead x = x
