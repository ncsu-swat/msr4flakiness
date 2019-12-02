import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.PackageDeclaration;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.expr.FieldAccessExpr;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.expr.StringLiteralExpr;
import com.github.javaparser.ast.stmt.BlockStmt;
import com.github.javaparser.ast.comments.LineComment;
import com.github.javaparser.ast.comments.BlockComment;

import java.io.FileInputStream;
import java.io.InputStream;
import java.io.ByteArrayInputStream;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;
import java.nio.charset.StandardCharsets;


public class Main {

    public static void listMethods(String fileName, String target) throws Exception {
        class MethodVisitor extends VoidVisitorAdapter<String> {
            @Override
            public void visit(MethodDeclaration md, String target) {
                super.visit(md, target);
                String s1 = md.getName().asString();
                if (s1.equals(target)) {
                    System.out.println(md);                    
                }
            }
        }
        FileInputStream in = new FileInputStream(fileName);
        CompilationUnit compUnit;
        try {
            compUnit = StaticJavaParser.parse(in);
            compUnit.accept(new MethodVisitor(), target);
        } finally {
            in.close();
        }
    }
    

    public static void main(String[] args) throws Exception {
        Main.listMethods(args[0], args[1]);
    }
}
