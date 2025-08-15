module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2021: true,
  },
  extends: ['eslint:recommended'],
  overrides: [
    {
      files: ['frontend/**/*.ts'],
      parser: '@typescript-eslint/parser',
      parserOptions: {
        project: './tsconfig.json',
      },
      plugins: ['@typescript-eslint'],
      extends: ['plugin:@typescript-eslint/recommended'],
    },
  ],
};
