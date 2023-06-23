from langchain.prompts import PromptTemplate

question_prompt_template = """Use the following summary of a portion of a long document to see if any of the text is relevant to answer the question.
Return any relevant summary.
{context}
Question: {question}
Relevant text, if any:"""
QUESTION_PROMPT = PromptTemplate(
    template=question_prompt_template, input_variables=["context", "question"]
)

combine_prompt_template = """Given the following summaries of parts of a long document and a question, create a final answer with references ("SOURCES").
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
ALWAYS return a "SOURCES" part in your answer.

QUESTION: What React components are implemented in the project?
=========
Summary: This code is a React component that renders a footer section. It includes links to a changelog and GitHub, displays the license information, and provides download links for Apple, Windows, and Linux. The footer also includes a Vercel logo link.
Source: /Users/shadowjack/Documents/work/python/hyper-site/components/footer/index.js
Summary: This code is a React component that renders a search list of plugins based on a search query. It imports the necessary dependencies and uses the `useSearch` hook from the `search-context` library to get the search query. It then filters the `allPlugins` array based on the search query and renders the filtered plugins if there are any. If there are no matching plugins, it displays an error message. The component also updates the page title based on the search query.
Source: /Users/shadowjack/Documents/work/python/hyper-site/components/search-list/index.js
Summary: This code is a React component that renders a page for showcasing the newest themes. It imports a component called `PluginThemeShowcase` and an array of plugins from a file called `plugins`. The `ThemeNewestPage` component receives a prop called `themes` and renders the `PluginThemeShowcase` component with the `themes` prop, as well as the `variant` and `filter` props set to "theme" and "newest" respectively. \n\nThe code also exports a function called `getStaticProps` which filters the `allPlugins` array to only include plugins of type "theme" and sorts them based on their `dateAdded` property in descending order. The sorted themes are then returned as the `themes` prop in the `getStaticProps` function.
Source: /Users/shadowjack/Documents/work/python/hyper-site/pages/themes/newest.js
=========
FINAL ANSWER: There are a few React components implemented in the project. Here are a few of them: a React component that renders a footer section, a React component that renders a search list of plugins based on a search query, a React component that renders a page for showcasing the newest themes
SOURCES: /Users/shadowjack/Documents/work/python/hyper-site/components/footer/index.js;/Users/shadowjack/Documents/work/python/hyper-site/components/search-list/index.js;/Users/shadowjack/Documents/work/python/hyper-site/pages/themes/newest.js

QUESTION: Which version of Node.js is being used?
=========
Summary: The code provides an overview of the Extensions API for a Node.js module called Hyper. It explains that extensions are loaded by both Electron and the renderer process. The code emphasizes the use of composition with React components and Redux actions to build the terminal. It also mentions that instead of exposing custom API methods or parameters, the code allows interception and composition of functionality. The code states that knowledge of the underlying open source libraries is required to successfully extend Hyper. Additionally, it provides a link to the Hyper repository for more details on plugin development. The code concludes by mentioning that the module needs to expose at least one method.
Source: /Users/shadowjack/Documents/work/python/hyper-site/pages/index.js
Summary: The code is using the `@next/mdx` package to enable support for MDX files in Next.js. It configures the `pageExtensions` to include both JavaScript and MDX files.
Source: /Users/shadowjack/Documents/work/python/hyper-site/next.config.js
Summary: This code is a JSON file that contains the configuration and dependencies for a project called "hyper-site". It includes information such as the project name, version, description, repository, and license. It also defines scripts for development, building, and starting the project. The dependencies and devDependencies sections list the required packages for the project. Additionally, there is a configuration for the Prettier code formatter and a Husky hook for running lint-staged before committing changes.
Source: /Users/shadowjack/Documents/work/python/hyper-site/package.json
=========
FINAL ANSWER: It's not possible to detect the Node.js version.
SOURCES:

QUESTION: {question}
=========
{summaries}
=========
FINAL ANSWER:"""
COMBINE_PROMPT = PromptTemplate(
    template=combine_prompt_template, input_variables=["summaries", "question"]
)

DOCUMENT_PROMPT = PromptTemplate(
        template="Summary: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)
