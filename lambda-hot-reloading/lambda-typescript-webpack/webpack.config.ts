import * as path from "path";
import * as webpack from "webpack";
import * as nodeBuiltins from "builtin-modules";

const DIST_DIR = path.join(__dirname, "dist");
const NodemonPlugin = require('nodemon-webpack-plugin');

const externals: webpack.Configuration["externals"] = ([] as string[])
  .concat(nodeBuiltins)
  .reduce((externalsMap, moduleName) => {
    externalsMap[moduleName] = moduleName;
    return externalsMap;
  }, {} as { [k: string]: string });

const config: webpack.Configuration = {
  mode: "production",
  target: "node",
  entry: {
    api: "./src/api.ts",
  },
  output: {
    path: DIST_DIR,
    filename: "[name].js",
    libraryTarget: "umd",
  },
  resolve: {
    extensions: [".mjs", ".ts", ".js"],
  },
  module: {
    rules: [
      { test: /\.ts$/, loader: "ts-loader" },
      // See https://github.com/apollographql/apollo-link-state/issues/302
      { test: /\.mjs$/, include: /node_modules/, type: "javascript/auto" },
    ],
    // https://github.com/webpack/webpack/issues/3078
    noParse: /iconv-loader\.js/,
  },
  plugins: [
    new NodemonPlugin(),
  ],
  externals,
};

export default config;
