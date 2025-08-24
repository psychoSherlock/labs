import { NextResponse } from "next/server";

export function middleware(request) {
  const protectedPaths = ["/will"];
  const path = request.nextUrl.pathname;

  if (protectedPaths.some((prefix) => path.startsWith(prefix))) {
    return NextResponse.redirect(new URL("/unauthorized", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
