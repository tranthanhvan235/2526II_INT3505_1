import "@typespec/http";

using Http;

@route("/books")
namespace BookAPI {

  @get op listBooks(): string[];

  @post op createBook(): string;

  @route("/{id}")
  @get op getBook(@path id: string): string;

  @put op updateBook(@path id: string): string;

  @delete op deleteBook(@path id: string): void;
}