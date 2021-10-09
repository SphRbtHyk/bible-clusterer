import type { NextPage } from "next";
import Head from "next/head";
import { Stack, Container } from "@chakra-ui/layout";
import BookCheckboxes from "../components/BookCheckbox";

const Home: NextPage = () => {
  return (
    <div>
      <Head>
        <title>LXX clusterer</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Stack h="100vh" bgColor="beige" alignItems="center">
        <BookCheckboxes></BookCheckboxes>
      </Stack>
    </div>
  );
};

export default Home;
