import "@typespec/http";

using Http;

@service({ title: "Book API" })
@route("/books")
namespace BookAPI {

  model Book {
    id: string;
    title: string;
    author: string;
  }

  @get
  op listBooks(): Book[];

  @post
  op createBook(@body book: Book): Book;

  @route("/{id}")
  @get
  op getBook(@path id: string): Book;

  @put
  op updateBook(@path id: string, @body book: Book): Book;

  @delete
  op deleteBook(@path id: string): void;
}