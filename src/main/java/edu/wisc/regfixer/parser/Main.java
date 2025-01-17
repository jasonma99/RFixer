package edu.wisc.regfixer.parser;

import java.io.StringReader;

import java_cup.runtime.Symbol;

import edu.wisc.regfixer.parser.Yylex;
import edu.wisc.regfixer.parser.parser;

public class Main {
  public static RegexNode parse (String raw) throws Exception {
    StringReader reader = new StringReader(raw);
    Yylex l = new Yylex(reader);
    parser p = new parser(l);
    Symbol s = p.parse();

    return (RegexNode)s.value;
  }
}
