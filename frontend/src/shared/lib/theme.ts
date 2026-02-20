export const applyTheme = (pathname: string) => {
  if (pathname.startsWith('/conversations')) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
};
