{-# LANGUAGE OverloadedStrings #-}
module PandocDemo where

import Data.Monoid ((<>))
import Data.Profunctor (dimap)
import Data.Text (Text)
import qualified Data.Text as T

import Text.Pandoc

markdownToHtml :: Text -> Text
markdownToHtml = dimap inp out markdownToHtml'
  where
    inp = T.unpack
    out = either (("Error: " <>) . tshow) T.pack

markdownToHtml' :: String -> Either PandocError String
markdownToHtml' s = writeHtmlString opts <$> readMarkdown def s
  where
    opts = def { writerHtml5 = True }


import Text.Pandoc

myWriterOptions = defaultWriterOptions 
    { writerHtml5 = True 
    , writerStrictMarkdown = False
    }

markdownToHtml :: String -> Html
markdownToHtml = writeHtml myWriterOptions . readMarkdown defaultParserState

-- table to collect elements in a line
local elements_in_line = {}

-- produce a span from the collected elements
local function line_as_span()
  local span = pandoc.Span(elements_in_line)
  elements_in_line = {}
  return span
end

local lines_to_blocks = {
  Inline = function (el)
    print(el.t)
    if el.t == 'SoftBreak' then
      return line_as_span()
    end
    table.insert(elements_in_line, el)
    return {}
  end,

  Para = function (el)
    local resources = {}
    local content = el.content
    -- last line is not followed by SoftBreak, add it here
    table.insert(content, line_as_span())
    local attr = pandoc.Attr('', {'Resource'})
    for i, line in ipairs(content) do
      resources[i] = pandoc.Div(pandoc.Plain(line.content), attr)
    end
    return resources
  end
}

function Div (el)
  -- return div unaltered unless it is of class "Resources"
  if not el.classes:includes'Resources' then
    return nil
  end
  return pandoc.walk_block(el, lines_to_blocks)
end


