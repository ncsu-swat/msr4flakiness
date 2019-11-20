import japa.parser.ASTHelper;
import japa.parser.JavaParser;
import japa.parser.ast.CompilationUnit;
import japa.parser.ast.PackageDeclaration;
import japa.parser.ast.body.ClassOrInterfaceDeclaration;
import japa.parser.ast.body.MethodDeclaration;
import japa.parser.ast.body.ModifierSet;
import japa.parser.ast.body.Parameter;
import japa.parser.ast.expr.FieldAccessExpr;
import japa.parser.ast.expr.MethodCallExpr;
import japa.parser.ast.expr.NameExpr;
import japa.parser.ast.expr.StringLiteralExpr;
import japa.parser.ast.stmt.BlockStmt;
import japa.parser.ast.visitor.VoidVisitorAdapter;

import java.io.FileInputStream;
import java.io.InputStream;
import java.io.ByteArrayInputStream;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;
import java.nio.charset.StandardCharsets;


public class Main {

    public static void listMethods(String contents, String target) throws Exception {
        class MethodVisitor extends VoidVisitorAdapter<String> {
            @Override
            public void visit(MethodDeclaration md, String target) {
                super.visit(md, target);
                if (md.getName().equals(target)) {
                    System.out.println(md);                    
                }
            }
        }
        FileInputStream in = new FileInputStream(contents);
        //InputStream in = new ByteArrayInputStream(contents.getBytes(StandardCharsets.UTF_8));
        CompilationUnit compUnit;
        try {
            compUnit = JavaParser.parse(in);
            compUnit.accept(new MethodVisitor(), target);
        } finally {
            in.close();
        }
    }
    

    public static void main(String[] args) throws Exception {
        //"/tmp/A.java", "allocateChars"        
        Main.listMethods(args[0], args[1]);
    }
}
