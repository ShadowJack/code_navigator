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
Code: import {{ Apple, Linux, Windows }} from \'../icons\'\nimport styles from \'./footer.module.css\'\n\nexport default () => (\n  <footer className={{styles.root}}>\n    <nav className={{styles.content}}>\n      <div className={{styles.left}}>\n        <a\n          target="_blank"\n          rel="noopener noreferrer"\n          href="https://github.com/vercel/hyper/releases"\n        >\n          Changelog\n        </a>\n        <a\n          target="_blank"\n          rel="noopener noreferrer"\n          href="https://github.com/vercel/hyper"\n        >\n          GitHub\n        </a>\n        <span>\n          License:&nbsp;<b>MIT</b>\n        </span>\n        <span className={{styles.download}}>\n          Download for:\n          <a href="/#installation" aria-label="Apple">\n            <Apple size={{16}} />\n          </a>\n          <a href="/#installation" aria-label="Windows">\n            <Windows size={{16}} />\n          </a>\n          <a href="/#installation" aria-label="Linux">\n            <Linux size={{16}} />\n          </a>\n        </span>\n      </div>\n\n      <a\n        target="_blank"\n        rel="noopener noreferrer"\n        className={{styles.logo}}\n        href="https://vercel.com"\n      >\n        ▲\n      </a>\n    </nav>\n  </footer>\n)
Summary: This code is a React component that renders a search list of plugins based on a search query. It imports the necessary dependencies and uses the `useSearch` hook from the `search-context` library to get the search query. It then filters the `allPlugins` array based on the search query and renders the filtered plugins if there are any. If there are no matching plugins, it displays an error message. The component also updates the page title based on the search query.
Source: /Users/shadowjack/Documents/work/python/hyper-site/components/search-list/index.js
Code: import Head from \'next/head\'\nimport PluginsList from \'../plugin-list\'\nimport styles from \'./search-list.module.css\'\nimport allPlugins from \'plugins\'\nimport {{ useSearch }} from \'lib/search-context\'\n\nexport default () => {{\n  const {{ search: query }} = useSearch()\n  const plugins = allPlugins.filter(\n    ({{ name, description }}) =>\n      name.includes(query) || description.includes(query)\n  )\n\n  if (plugins.length > 0) {{\n    return (\n      <>\n        <Head>\n          <title>{{`Hyper™ Store - Searching for "${{query}}"`}}</title>\n        </Head>\n        <PluginsList plugins={{plugins}} query={{query}} />\n      </>\n    )\n  }}\n\n  return (\n    <>\n      <Head>\n        <title>{{`Hyper™ Store - No results for "${{query}}"`}}</title>\n      </Head>\n      <div className={{styles.searchError}}>\n        Your search for "<b>{{query}}</b>" did not match any plugins or themes 😱{{\' \'}}\n        <br />\n        Make sure the search term is spelled correctly.\n      </div>\n    </>\n  )\n}}
Summary: This code is a React component that renders a page for showcasing the newest themes. It imports a component called `PluginThemeShowcase` and an array of plugins from a file called `plugins`. The `ThemeNewestPage` component receives a prop called `themes` and renders the `PluginThemeShowcase` component with the `themes` prop, as well as the `variant` and `filter` props set to "theme" and "newest" respectively. \n\nThe code also exports a function called `getStaticProps` which filters the `allPlugins` array to only include plugins of type "theme" and sorts them based on their `dateAdded` property in descending order. The sorted themes are then returned as the `themes` prop in the `getStaticProps` function.
Source: /Users/shadowjack/Documents/work/python/hyper-site/pages/themes/newest.js
Code: import PluginThemeShowcase from \'components/plugin-theme-showcase\'\nimport allPlugins from \'plugins\'\n\nexport default function ThemeNewestPage({{ themes }}) {{\n  return (\n    <PluginThemeShowcase plugins={{themes}} variant="theme" filter="newest" />\n  )\n}}\n\nexport function getStaticProps() {{\n  const themes = allPlugins\n    .filter((p) => p.type === \'theme\')\n    .sort((a, b) =>\n      a.dateAdded < b.dateAdded ? 1 : a.dateAdded > b.dateAdded ? -1 : 0\n    )\n\n  return {{\n    props: {{\n      themes,\n    }},\n  }}\n}}
=========
FINAL ANSWER: There are a few React components implemented in the project. Here are a few of them: a React component that renders a footer section, a React component that renders a search list of plugins based on a search query, a React component that renders a page for showcasing the newest themes
SOURCES: /Users/shadowjack/Documents/work/python/hyper-site/components/footer/index.js;/Users/shadowjack/Documents/work/python/hyper-site/components/search-list/index.js;/Users/shadowjack/Documents/work/python/hyper-site/pages/themes/newest.js

QUESTION: Which version of Node.js is being used?
=========
Summary: The code provides an overview of the Extensions API for a Node.js module called Hyper. It explains that extensions are loaded by both Electron and the renderer process. The code emphasizes the use of composition with React components and Redux actions to build the terminal. It also mentions that instead of exposing custom API methods or parameters, the code allows interception and composition of functionality. The code states that knowledge of the underlying open source libraries is required to successfully extend Hyper. Additionally, it provides a link to the Hyper repository for more details on plugin development. The code concludes by mentioning that the module needs to expose at least one method.
Source: /Users/shadowjack/Documents/work/python/hyper-site/pages/index.js
Code: {{/**\n         * Extensions API\n         */}}\n        <h2 id="extensions-api">\n          <a href="#extensions-api">Extensions API</a>\n        </h2>\n        <p>\n          Extensions are universal Node.js modules loaded by both Electron and\n          the renderer process.\n        </p>\n        <p>\n          The extension system is designed around <b>composition</b> of the APIs\n          we use to build the terminal: <code>React</code> components and{{\' \'}}\n          <code>Redux</code> actions.\n        </p>\n        <p>\n          Instead of exposing a custom API method or parameter for every\n          possible customization point, we allow you to intercept and compose\n          every bit of functionality!\n        </p>\n        <p>\n          The only knowledge that is therefore required to successfully extend{{\' \'}}\n          <code>Hyper</code> is that of its underlying open source libraries.\n        </p>\n        <p>\n          You can find additional details about plugin development{{\' \'}}\n          <a href="https://github.com/vercel/hyper/blob/master/PLUGINS.md">\n            in the Hyper repository\n          </a>\n          .\n        </p>\n        <p>Your module has to expose at least one of these methods:</p>\n        <div className="table large">\n          <table className="api">\n            <thead>\n              <tr>\n                <td>Method</td>
Summary: The code is using the `@next/mdx` package to enable support for MDX files in Next.js. It configures the `pageExtensions` to include both JavaScript and MDX files.
Source: /Users/shadowjack/Documents/work/python/hyper-site/next.config.js
Code: const withMDX = require('@next/mdx')({{\n  extension: /\\.mdx?$/,\n}})\n\nmodule.exports = withMDX({{\n  pageExtensions: ['js', 'mdx'],\n}})
Summary: This code is a JSON file that contains the configuration and dependencies for a project called "hyper-site". It includes information such as the project name, version, description, repository, and license. It also defines scripts for development, building, and starting the project. The dependencies and devDependencies sections list the required packages for the project. Additionally, there is a configuration for the Prettier code formatter and a Husky hook for running lint-staged before committing changes.
Source: /Users/shadowjack/Documents/work/python/hyper-site/package.json
Code: {{\n  "name": "hyper-site",\n  "private": true,\n  "version": "1.3.0",\n  "description": "The official website for the Hyper terminal",\n  "repository": "vercel/hyper-site",\n  "license": "MIT",\n  "scripts": {{\n    "dev": "next dev",\n    "build": "node generate-plugin-images-metadata.js && next build",\n    "start": "next start"\n  }},\n  "dependencies": {{\n    "@mdx-js/loader": "^1.6.4",\n    "@mdx-js/react": "^1.6.4",\n    "@next/mdx": "^9.4.2",\n    "copee": "^1.0.6",\n    "husky": "^4.2.5",\n    "image-size": "^0.9.3",\n    "lint-staged": "^10.2.3",\n    "next": "^13.0.5",\n    "nprogress": "^0.2.0",\n    "react": "^18.2.0",\n    "react-dom": "^18.2.0",\n    "react-gravatar": "^2.6.3",\n    "react-highlighter": "^0.4.3"\n  }},\n  "devDependencies": {{\n    "prettier": "^2.0.5",\n    "shell-quote": "^1.7.2"\n  }},\n  "prettier": {{\n    "singleQuote": true,\n    "semi": false\n  }},\n  "husky": {{\n    "hooks": {{\n      "pre-commit": "lint-staged"\n    }}\n  }}\n}}
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
        template="Summary: {page_content}\nSource: {source}\nCode: {text}",
    input_variables=["page_content", "source", "text"],
)
