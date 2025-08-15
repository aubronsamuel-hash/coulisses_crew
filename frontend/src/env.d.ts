interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  [key: string]: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
